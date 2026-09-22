from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from safeagent.agent.agent import parse_trusted_request
from safeagent.bootstrap import bootstrap
from safeagent.runtime.authorization import TrustedIdentity
from safeagent.runtime.schemas import ActionProposal
from safeagent.sandbox.models import File, Task
from safeagent.settings import Settings


@pytest.fixture
def gateway(tmp_path):
    gateway = bootstrap(Settings(database_url=f"sqlite:///{tmp_path / 'test.db'}"))
    yield gateway
    gateway.engine.dispose()


@pytest.fixture
def task_factory(gateway):
    def create(request="Rename FILE-001 to Reviewed report"):
        template, scope = parse_trusted_request(request)
        identity = TrustedIdentity("USER-001", str(uuid4()))
        task_id = str(uuid4())
        with Session(gateway.engine) as db, db.begin():
            db.add(
                Task(
                    id=task_id,
                    session_id=identity.session_id,
                    user_id=identity.user_id,
                    request=request,
                    template=template,
                    scope=scope,
                    status="PLANNING",
                )
            )
        return identity, task_id

    return create


@pytest.fixture
def proposal_factory(task_factory):
    def create(request="Rename FILE-001 to Reviewed report", **kwargs):
        identity, task_id = task_factory(request)
        values = {
            "tool_name": "update_file",
            "arguments": {
                "file_id": "FILE-001",
                "changes": {"title": "Reviewed report"},
                "expected_version": 1,
            },
        }
        values.update(kwargs)
        return identity, ActionProposal(task_id=task_id, session_id=identity.session_id, **values)

    return create


@pytest.fixture
def snapshot(gateway):
    def take():
        with Session(gateway.engine) as db:
            return [
                (f.id, f.title, f.content, f.version)
                for f in db.scalars(select(File).order_by(File.id))
            ]

    return take
