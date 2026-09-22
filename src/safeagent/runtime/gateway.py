"""Single agent-facing execution boundary. The caller supplies a trusted identity separately."""

from threading import RLock

from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from safeagent.runtime.authorization import TrustedIdentity, load_context
from safeagent.runtime.policy import PolicyEngine
from safeagent.runtime.schemas import ActionProposal, Decision, GatewayResult
from safeagent.runtime.state_machine import State, transition
from safeagent.sandbox.models import AuditEvent, Execution, now
from safeagent.sandbox.tools import REGISTRY, StaleResourceError


class ProposalValidationError(ValueError):
    """Schema/interface failure, distinct from an ordinary policy BLOCK."""


def audit(db: Session, task_id: str, kind: str, details: dict, action_id: str | None = None):
    db.add(AuditEvent(task_id=task_id, action_id=action_id, kind=kind, details=details))


class Gateway:
    def __init__(self, engine: Engine, policy: PolicyEngine):
        self.engine = engine
        self.policy = policy
        self.lock = RLock()

    def execute(self, proposal: ActionProposal, identity: TrustedIdentity) -> GatewayResult:
        spec = REGISTRY.get(proposal.tool_name)
        if spec is None:
            raise ProposalValidationError("UNKNOWN_TOOL")
        try:
            args = spec.argument_schema.model_validate(proposal.arguments)
        except ValidationError as exc:
            # Do not echo attacker-controlled arguments or secret-like values in errors.
            raise ProposalValidationError("INVALID_TOOL_ARGUMENTS") from exc
        if proposal.session_id != identity.session_id:
            raise ProposalValidationError("SESSION_MISMATCH")
        if proposal.target_resource_ids and proposal.target_resource_ids != [args.file_id]:
            raise ProposalValidationError("RESOURCE_CLAIM_MISMATCH")

        with self.lock, Session(self.engine, expire_on_commit=False) as db:
            db.execute(text("BEGIN IMMEDIATE"))
            context = load_context(db, identity, proposal.task_id)
            if db.get(Execution, proposal.action_id):
                raise ProposalValidationError("DUPLICATE_ACTION_ID")
            record = Execution(
                action_id=proposal.action_id,
                task_id=proposal.task_id,
                tool_name=spec.name,
                arguments=args.model_dump(),
                resource_ids=[args.file_id],
                state=State.PROPOSED,
            )
            db.add(record)
            audit(
                db,
                proposal.task_id,
                "AGENT_PROPOSAL",
                {
                    "tool_name": spec.name,
                    "arguments": args.model_dump(),
                    "provenance": "UNTRUSTED_AGENT_PROPOSAL",
                },
                proposal.action_id,
            )
            transition(record, State.VALIDATING)
            audit(db, proposal.task_id, "VALIDATION", {"valid": True}, proposal.action_id)
            decision = self.policy.evaluate(db, proposal, args, spec, context)
            record.decision = decision.model_dump(mode="json")
            audit(db, proposal.task_id, "POLICY_DECISION", record.decision, proposal.action_id)
            if decision.decision != Decision.ALLOW:
                transition(record, State.BLOCKED)
                record.finished_at = now()
                db.commit()
                return GatewayResult(
                    action_id=record.action_id, state=record.state, decision=decision
                )
            transition(record, State.APPROVED)
            transition(record, State.EXECUTING)
            # Persist intent BEFORE entering the application tool transaction.
            db.commit()

            tool_started = False
            try:
                db.execute(text("BEGIN IMMEDIATE"))
                # Reevaluate server permissions and version under the SQLite write lock.
                context = load_context(db, identity, proposal.task_id)
                decision = self.policy.evaluate(db, proposal, args, spec, context)
                record.decision = decision.model_dump(mode="json")
                if decision.decision != Decision.ALLOW:
                    transition(record, State.BLOCKED)
                    record.finished_at = now()
                    audit(
                        db, proposal.task_id, "POLICY_DECISION", record.decision, proposal.action_id
                    )
                    db.commit()
                    return GatewayResult(
                        action_id=record.action_id, state=record.state, decision=decision
                    )
                record.attempts = 1
                tool_started = True
                audit(db, proposal.task_id, "TOOL_EXECUTION", {"attempt": 1}, proposal.action_id)
                response = spec.response_schema.model_validate(spec.execute(db, args))
                if not spec.verify(db, args, response):
                    raise ValueError("State verification failed")
                output = response.model_dump()
                record.response = response.model_dump(exclude={"content"})
                record.verified = True
                transition(record, State.SUCCEEDED)
                record.finished_at = now()
                audit(
                    db,
                    proposal.task_id,
                    "EXECUTION_VERIFICATION",
                    {
                        "verified": True,
                        "observed_state": record.response,
                    },
                    proposal.action_id,
                )
                # Local sandbox effects and verified receipt commit atomically.
                db.commit()
                return GatewayResult(
                    action_id=record.action_id,
                    state=record.state,
                    decision=decision,
                    output=output,
                    verified=True,
                )
            except Exception as exc:
                db.rollback()
                record = db.get(Execution, proposal.action_id, populate_existing=True)
                # A failed commit may have succeeded. Do not overwrite a durable success.
                if record.state == State.SUCCEEDED and record.verified:
                    return GatewayResult(
                        action_id=record.action_id,
                        state=record.state,
                        decision=decision,
                        output=record.response,
                        verified=True,
                    )
                known = isinstance(
                    exc, (ValueError, LookupError, StaleResourceError, PermissionError)
                )
                transition(record, State.FAILED if known else State.OUTCOME_UNKNOWN)
                record.attempts = int(tool_started)
                record.error_code = (
                    "TOOL_EXECUTION_FAILED" if known else "UNKNOWN_EXECUTION_OUTCOME"
                )
                record.finished_at = now()
                if tool_started:
                    # The failed application transaction rolled back its initial attempt event.
                    audit(
                        db,
                        proposal.task_id,
                        "TOOL_EXECUTION",
                        {
                            "attempt": 1,
                            "error": True,
                        },
                        proposal.action_id,
                    )
                audit(
                    db,
                    proposal.task_id,
                    "EXECUTION_VERIFICATION",
                    {
                        "verified": False,
                        "state": record.state,
                        "error_code": record.error_code,
                    },
                    proposal.action_id,
                )
                db.commit()
                return GatewayResult(
                    action_id=record.action_id,
                    state=record.state,
                    decision=decision,
                    error_code=record.error_code,
                )
