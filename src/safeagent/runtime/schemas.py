from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


def identifier() -> str:
    return str(uuid4())


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class ActionProposal(StrictModel):
    action_id: str = Field(default_factory=identifier, min_length=1, max_length=128)
    session_id: str
    task_id: str
    tool_name: str = Field(min_length=1, max_length=80)
    arguments: dict[str, Any]
    target_resource_ids: list[str] = Field(default_factory=list)
    requested_effect: str = ""
    agent_reason: str = ""
    evidence_references: list[str] = Field(default_factory=list)
    expected_outcome: str = ""


class Decision(StrEnum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    CLARIFY = "CLARIFY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


class SafetyDecision(StrictModel):
    decision_id: str = Field(default_factory=identifier)
    action_id: str
    decision: Decision
    reason_codes: list[str]
    human_readable_explanation: str
    policy_ids: list[str]
    risk_category: str | None = None
    confidence_or_uncertainty: str = "Deterministic policy; no model confidence inferred."
    required_user_input: str | None = None
    approval_request_id: str | None = None
    evaluated_resource_versions: dict[str, int] = Field(default_factory=dict)
    timestamp: datetime


class GatewayResult(StrictModel):
    action_id: str
    state: str
    decision: SafetyDecision | None = None
    output: dict[str, Any] | None = None
    error_code: str | None = None
    verified: bool = False
