import json
from pathlib import Path

from pydantic import Field
from sqlalchemy.orm import Session

from safeagent.runtime.authorization import AuthorizationContext
from safeagent.runtime.schemas import ActionProposal, Decision, SafetyDecision, StrictModel
from safeagent.sandbox.models import File, Permission, now
from safeagent.sandbox.tools import ReadFile, ToolSpec, UpdateFile


class PolicyConfig(StrictModel):
    version: str
    allowed_tools: list[str]
    max_title_length: int = Field(ge=1, le=160)

    @classmethod
    def load(cls, path: Path) -> "PolicyConfig":
        return cls.model_validate(json.loads(path.read_text(encoding="utf-8")))


class PolicyEngine:
    def __init__(self, config: PolicyConfig):
        self.config = config

    def evaluate(
        self,
        db: Session,
        proposal: ActionProposal,
        args: ReadFile,
        spec: ToolSpec,
        context: AuthorizationContext,
    ) -> SafetyDecision:
        resource = db.get(File, args.file_id, populate_existing=True)
        versions = {resource.id: resource.version} if resource else {}

        def decision(code: str, explanation: str, allow: bool = False) -> SafetyDecision:
            return SafetyDecision(
                action_id=proposal.action_id,
                decision=Decision.ALLOW if allow else Decision.BLOCK,
                reason_codes=[code],
                human_readable_explanation=explanation,
                policy_ids=[self.config.version + ":" + code],
                evaluated_resource_versions=versions,
                timestamp=now(),
            )

        if spec.name not in self.config.allowed_tools:
            return decision("TOOL_DISABLED", "This operation is disabled by server policy.")
        if spec.permission not in context.granted_operations:
            return decision(
                "TASK_OPERATION_DENIED", "The trusted task does not grant this operation."
            )
        if args.file_id not in context.permitted_resource_ids:
            return decision(
                "TASK_RESOURCE_DENIED", "This resource is outside the trusted task scope."
            )
        if not resource:
            return decision("RESOURCE_NOT_FOUND", "The authorized resource does not exist.")
        if not db.get(Permission, (context.user_id, spec.permission, args.file_id)):
            return decision(
                "RESOURCE_PERMISSION_DENIED", "Server-side resource permission is absent."
            )
        if isinstance(args, UpdateFile):
            exact = {"file_id": args.file_id, "changes": args.changes.model_dump()}
            if exact != context.exact_mutations:
                return decision(
                    "TASK_EFFECT_DENIED", "The proposed change differs from the trusted request."
                )
            if len(args.changes.title) > self.config.max_title_length:
                return decision(
                    "TITLE_POLICY_DENIED", "The title exceeds the configured policy limit."
                )
            if args.expected_version != resource.version:
                result = decision(
                    "STALE_RESOURCE_STATE", "Read the current state and submit a new proposal."
                )
                result.risk_category = "STALE_RESOURCE_STATE"
                return result
        return decision(
            "AUTHORIZED", "Operation, resource, and concrete effect satisfy server policy.", True
        )
