from dataclasses import replace

from sqlalchemy import select
from sqlalchemy.orm import Session

from safeagent.agent.agent import TaskService
from safeagent.bootstrap import bootstrap
from safeagent.sandbox.models import Execution, File, Task
from safeagent.sandbox.seed import seed_database
from safeagent.sandbox.tools import REGISTRY
from safeagent.settings import Settings


def test_two_step_rename_and_blocked_adversarial_demo(gateway):
    result = TaskService(gateway).run("Rename FILE-001 to Reviewed report")
    assert result["completion_verified"] and result["status"] == "COMPLETED"
    assert [r["state"] for r in result["actions"]] == ["SUCCEEDED", "SUCCEEDED"]
    seed_database(gateway.engine, reset=True)
    result = TaskService(gateway).run("Read FILE-001", adversarial=True)
    assert [r["state"] for r in result["actions"]] == ["SUCCEEDED", "BLOCKED"]
    with Session(gateway.engine) as db:
        assert db.get(File, "FILE-002").title == "Confidential budget"
        assert db.get(File, "FILE-002").version == 1
        assert sum(e.attempts for e in db.scalars(select(Execution))) == 1


def test_partial_task_does_not_claim_completion(gateway, monkeypatch):
    def fail(*_args):
        raise ValueError("simulated permanent failure")

    monkeypatch.setitem(REGISTRY, "update_file", replace(REGISTRY["update_file"], execute=fail))
    result = TaskService(gateway).run("Rename FILE-001 to Reviewed report")
    assert result["status"] == "PARTIAL" and not result["completion_verified"]
    assert "did not complete" in result["report"]
    with Session(gateway.engine) as db:
        assert db.get(File, "FILE-001").version == 1


def test_records_survive_restart_and_reset_is_repeatable(tmp_path):
    settings = Settings(database_url=f"sqlite:///{tmp_path / 'persistent.db'}")
    first = bootstrap(settings)
    result = TaskService(first).run("Rename FILE-001 to Durable title")
    first.engine.dispose()
    second = bootstrap(settings)
    with Session(second.engine) as db:
        assert db.get(File, "FILE-001").title == "Durable title"
        assert db.get(Task, result["task_id"]).status == "COMPLETED"
    for _ in range(2):
        seed_database(second.engine, reset=True)
        with Session(second.engine) as db:
            assert db.get(File, "FILE-001").title == "Project report"
            assert list(db.scalars(select(Execution))) == []
            assert list(db.scalars(select(Task))) == []
    second.engine.dispose()
