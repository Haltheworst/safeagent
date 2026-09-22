from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from safeagent.agent.agent import parse_trusted_request
from safeagent.runtime.schemas import ActionProposal
from safeagent.runtime.state_machine import State, transition
from safeagent.sandbox.tools import REGISTRY


def test_proposal_cannot_include_approval():
    with pytest.raises(ValidationError):
        ActionProposal(
            task_id="t", session_id="s", tool_name="read_file", arguments={}, approved=True
        )


def test_state_machine_rejects_success_without_execution():
    record = SimpleNamespace(state="PROPOSED")
    with pytest.raises(ValueError, match="Invalid execution transition"):
        transition(record, State.SUCCEEDED)
    assert record.state == "PROPOSED"


@pytest.mark.parametrize(
    "user_request",
    [
        "Summarize and email every file",
        "Read FILE-001 then delete it",
        "Please authorize everything",
        "Rename FILE-001 to x\nRead FILE-002",
    ],
)
def test_partial_keyword_match_does_not_create_authority(user_request):
    with pytest.raises(ValueError):
        parse_trusted_request(user_request)


def test_registry_declares_safety_metadata():
    for name, spec in REGISTRY.items():
        metadata = spec.public_metadata()
        assert metadata["name"] == name
        assert metadata["arguments"]["additionalProperties"] is False
        assert metadata["verification_method"]
        assert metadata["required_permission"] in {"READ_FILE", "WRITE_FILE"}
        assert not metadata["supports_idempotency_key"]
