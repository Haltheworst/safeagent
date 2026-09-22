from dataclasses import replace

import pytest
from sqlalchemy.orm import Session

from safeagent.runtime.gateway import ProposalValidationError
from safeagent.runtime.policy import PolicyConfig, PolicyEngine
from safeagent.sandbox.models import Execution, File
from safeagent.sandbox.tools import REGISTRY


def test_failed_revalidation_is_not_counted_as_tool_attempt(
    gateway,
    proposal_factory,
    snapshot,
    monkeypatch,
):
    import safeagent.runtime.gateway as gateway_module

    original = gateway_module.load_context
    calls = []

    def revoked_on_revalidation(*args):
        calls.append(1)
        if len(calls) == 2:
            raise PermissionError("Task authorization revoked before tool entry")
        return original(*args)

    monkeypatch.setattr(gateway_module, "load_context", revoked_on_revalidation)
    identity, proposal = proposal_factory()
    before = snapshot()
    result = gateway.execute(proposal, identity)
    assert result.state == "FAILED" and snapshot() == before
    with Session(gateway.engine) as db:
        assert db.get(Execution, proposal.action_id).attempts == 0


def test_permitted_operation_persists_verified_effect(gateway, proposal_factory):
    identity, proposal = proposal_factory()
    result = gateway.execute(proposal, identity)
    assert result.state == "SUCCEEDED" and result.verified
    with Session(gateway.engine) as db:
        assert db.get(File, "FILE-001").title == "Reviewed report"
        assert db.get(File, "FILE-001").version == 2
        record = db.get(Execution, proposal.action_id)
        assert record.verified and record.attempts == 1
        assert record.decision["evaluated_resource_versions"] == {"FILE-001": 1}


def test_execution_intent_is_durable_before_tool_call(gateway, proposal_factory, monkeypatch):
    original = REGISTRY["update_file"]
    identity, proposal = proposal_factory()

    def inspect_intent(db, args):
        with Session(gateway.engine) as reader:
            assert reader.get(Execution, proposal.action_id).state == "EXECUTING"
            assert reader.get(File, "FILE-001").version == 1
        return original.execute(db, args)

    monkeypatch.setitem(REGISTRY, "update_file", replace(original, execute=inspect_intent))
    assert gateway.execute(proposal, identity).verified


def test_repeated_action_id_never_reexecutes(gateway, proposal_factory, snapshot):
    identity, proposal = proposal_factory()
    gateway.execute(proposal, identity)
    before = snapshot()
    with pytest.raises(ProposalValidationError, match="DUPLICATE_ACTION_ID"):
        gateway.execute(proposal, identity)
    assert snapshot() == before


def test_stale_version_blocks_without_mutation(gateway, proposal_factory, snapshot):
    identity, proposal = proposal_factory()
    with Session(gateway.engine) as db, db.begin():
        db.get(File, "FILE-001").version = 2
    before = snapshot()
    result = gateway.execute(proposal, identity)
    assert result.decision.reason_codes == ["STALE_RESOURCE_STATE"]
    assert snapshot() == before
    with Session(gateway.engine) as db:
        assert db.get(Execution, proposal.action_id).attempts == 0


def test_invalid_tool_response_rolls_back_mutation(
    gateway, proposal_factory, snapshot, monkeypatch
):
    original = REGISTRY["update_file"]

    def invalid_response(db, args):
        original.execute(db, args)
        return {"success": True}

    monkeypatch.setitem(REGISTRY, "update_file", replace(original, execute=invalid_response))
    identity, proposal = proposal_factory()
    before = snapshot()
    result = gateway.execute(proposal, identity)
    assert result.state == "FAILED" and not result.verified
    assert snapshot() == before


def test_unknown_error_is_not_reported_success_or_blindly_retried(
    gateway,
    proposal_factory,
    snapshot,
    monkeypatch,
):
    calls = []

    def unknown_error(*_args):
        calls.append(1)
        raise OSError("simulated lost connection")

    monkeypatch.setitem(
        REGISTRY, "update_file", replace(REGISTRY["update_file"], execute=unknown_error)
    )
    identity, proposal = proposal_factory()
    before = snapshot()
    result = gateway.execute(proposal, identity)
    assert result.state == "OUTCOME_UNKNOWN" and not result.verified
    assert calls == [1] and snapshot() == before


def test_strict_policy_disables_mutations(gateway, proposal_factory, snapshot):
    gateway.policy = PolicyEngine(
        PolicyConfig(version="strict", allowed_tools=["read_file"], max_title_length=160)
    )
    identity, proposal = proposal_factory()
    before = snapshot()
    assert gateway.execute(proposal, identity).decision.reason_codes == ["TOOL_DISABLED"]
    assert snapshot() == before
