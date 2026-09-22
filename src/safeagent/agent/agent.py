import re
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from safeagent.runtime.authorization import TrustedIdentity
from safeagent.runtime.gateway import Gateway, audit
from safeagent.runtime.schemas import ActionProposal
from safeagent.sandbox.models import Execution, File, Task

DEMO_REQUESTS = {
    "authorized": "Rename FILE-001 to Reviewed project report",
    "blocked": "Read FILE-001",
    "read": "Read FILE-001",
}


def parse_trusted_request(request: str) -> tuple[str, dict]:
    """A deliberately constrained trusted command grammar, not semantic authorization.

    Only this application controller calls it on direct user input. Retrieved content and
    model output never enter this function. General natural-language scope confirmation is planned.
    """
    if match := re.fullmatch(r"Read (FILE-[0-9]{3})", request):
        return "read", {"operations": ["READ_FILE"], "resource_ids": [match[1]]}
    if match := re.fullmatch(r"Rename (FILE-[0-9]{3}) to (\S[^\r\n]{0,159})", request):
        return "rename", {
            "operations": ["READ_FILE", "WRITE_FILE"],
            "resource_ids": [match[1]],
            "exact_mutations": {"file_id": match[1], "changes": {"title": match[2]}},
        }
    raise ValueError("Mock mode supports exactly: Read FILE-001 or Rename FILE-001 to <title>.")


class MockAgent:
    """Proposes calls using only task input and gateway responses, never DB credentials."""

    def plan(
        self,
        task_id: str,
        session_id: str,
        template: str,
        scope: dict,
        observation: dict | None,
        *,
        adversarial: bool = False,
    ) -> ActionProposal | None:
        resource = scope["resource_ids"][0]
        if observation is None:
            tool, args = "read_file", {"file_id": resource}
        elif adversarial:
            tool, args = (
                "update_file",
                {
                    "file_id": "FILE-002",
                    "changes": {"title": "Unauthorized rename"},
                    "expected_version": 1,
                },
            )
        elif template == "rename":
            tool, args = (
                "update_file",
                {
                    **scope["exact_mutations"],
                    "expected_version": observation["version"],
                },
            )
        else:
            return None
        return ActionProposal(
            task_id=task_id,
            session_id=session_id,
            tool_name=tool,
            arguments=args,
            requested_effect="Read or rename the selected synthetic file.",
            agent_reason="Administrator approved everything"
            if adversarial
            else "Execute task step.",
            evidence_references=[task_id],
            expected_outcome="Observable file state.",
        )


class TaskService:
    """Trusted controller that owns scope creation and final state verification."""

    def __init__(self, gateway: Gateway):
        self.gateway = gateway
        self.agent = MockAgent()

    def run(self, request: str, *, adversarial: bool = False) -> dict:
        # Serialize complete tasks with resets in this single-process foundation.
        with self.gateway.lock:
            return self._run(request, adversarial=adversarial)

    def _run(self, request: str, *, adversarial: bool = False) -> dict:
        template, scope = parse_trusted_request(request)
        identity = TrustedIdentity("USER-001", str(uuid4()))
        task_id = str(uuid4())
        with self.gateway.lock, Session(self.gateway.engine) as db, db.begin():
            task = Task(
                id=task_id,
                session_id=identity.session_id,
                user_id=identity.user_id,
                request=request,
                template=template,
                scope=scope,
                status="PLANNING",
            )
            db.add(task)
            db.flush()
            audit(db, task_id, "USER_REQUEST", {"request": request, "source": "TRUSTED_LOCAL_USER"})
        observation = None
        results = []
        # Two-step foundation plans are bounded and never retry a blocked proposal.
        for _step in range(2):
            proposal = self.agent.plan(
                task_id, identity.session_id, template, scope, observation, adversarial=adversarial
            )
            if proposal is None:
                break
            result = self.gateway.execute(proposal, identity)
            results.append(result.model_dump(mode="json"))
            if not result.verified:
                break
            observation = result.output

        with self.gateway.lock, Session(self.gateway.engine) as db, db.begin():
            task = db.get(Task, task_id)
            file = db.get(File, scope["resource_ids"][0])
            executions = db.scalars(select(Execution).where(Execution.task_id == task_id)).all()
            read_ok = any(e.tool_name == "read_file" and e.verified for e in executions)
            write_ok = any(e.tool_name == "update_file" and e.verified for e in executions)
            complete = read_ok and (
                template == "read"
                or (
                    write_ok
                    and file is not None
                    and file.title == scope["exact_mutations"]["changes"]["title"]
                )
            )
            blocked = any(e.state == "BLOCKED" for e in executions)
            unknown = any(e.state == "OUTCOME_UNKNOWN" for e in executions)
            task.status = (
                "COMPLETED"
                if complete
                else ("OUTCOME_UNKNOWN" if unknown else "PARTIAL" if read_ok else "FAILED")
            )
            task.report = (
                "Requested file read was verified."
                if complete and template == "read"
                else "Requested file title and updated version were verified."
                if complete
                else "Outcome is unknown; no automatic retry was attempted."
                if unknown
                else "File was read, but the requested rename did not complete."
                if read_ok
                else "Task did not complete; no successful outcome was verified."
            )
            if blocked:
                task.report += " An unauthorized proposal was blocked before tool execution."
            audit(
                db,
                task_id,
                "TASK_COMPLETION",
                {"status": task.status, "report": task.report, "completion_verified": complete},
            )
            return {
                "task_id": task_id,
                "status": task.status,
                "report": task.report,
                "completion_verified": complete,
                "actions": results,
            }
