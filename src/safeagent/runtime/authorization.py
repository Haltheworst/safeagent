from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from safeagent.sandbox.models import Task


@dataclass(frozen=True)
class TrustedIdentity:
    """Created by the local application, never parsed from model arguments."""

    user_id: str
    session_id: str


@dataclass(frozen=True)
class AuthorizationContext:
    user_id: str
    session_id: str
    task_id: str
    trusted_request_reference: str
    granted_operations: frozenset[str]
    permitted_resource_ids: frozenset[str]
    exact_mutations: dict[str, Any]


def load_context(db: Session, identity: TrustedIdentity, task_id: str) -> AuthorizationContext:
    task = db.get(Task, task_id)
    if task is None or (task.user_id, task.session_id) != (identity.user_id, identity.session_id):
        raise PermissionError("Task does not belong to this trusted session.")
    if task.status not in {"PLANNING", "EXECUTING"}:
        raise PermissionError("Task is no longer active.")
    return AuthorizationContext(
        user_id=identity.user_id,
        session_id=identity.session_id,
        task_id=task.id,
        trusted_request_reference=task.id,
        granted_operations=frozenset(task.scope["operations"]),
        permitted_resource_ids=frozenset(task.scope["resource_ids"]),
        exact_mutations=task.scope.get("exact_mutations", {}),
    )
