import pytest
from fastapi.testclient import TestClient

from safeagent.main import create_app
from safeagent.settings import Settings

HEADERS = {"X-SafeAgent-Client": "local-ui"}


@pytest.fixture
def client(tmp_path):
    app = create_app(Settings(database_url=f"sqlite:///{tmp_path / 'api.db'}"))
    with TestClient(app) as client:
        yield client


def test_health_empty_metrics_and_real_workflow(client):
    assert client.get("/api/health").json()["status"] == "ok"
    assert client.get("/api/summary").json()["tasks"] == 0
    response = client.post(
        "/api/tasks", json={"request": "Rename FILE-001 to API title"}, headers=HEADERS
    )
    assert response.status_code == 200
    result = response.json()
    assert result["completion_verified"]
    assert client.get("/api/sandbox").json()["files"][0]["title"] == "API title"
    trace = client.get(f"/api/tasks/{result['task_id']}/trace").json()
    assert trace[-1]["kind"] == "TASK_COMPLETION"
    summary = client.get("/api/summary").json()
    assert summary["verified_executions"] == 2 and summary["evaluated_tasks"] == 0


def test_blocked_demo_counts_only_actual_attempts(client):
    result = client.post("/api/demos", json={"name": "blocked"}, headers=HEADERS).json()
    assert result["actions"][-1]["state"] == "BLOCKED"
    summary = client.get("/api/summary").json()
    assert summary["blocked_proposals"] == 1 and summary["tool_attempts"] == 1
    assert client.get("/api/sandbox").json()["files"][1]["version"] == 1


def test_no_api_for_model_auth_grants(client):
    response = client.post(
        "/api/tasks", json={"request": "Read FILE-001", "approved": True}, headers=HEADERS
    )
    assert response.status_code == 422
    assert client.post("/api/approvals", json={}, headers=HEADERS).status_code == 404
    assert client.get("/api/summary").json()["tasks"] == 0


def test_reset_requires_explicit_marker(client):
    assert client.post("/api/sandbox/reset", json={}, headers=HEADERS).status_code == 422
    assert (
        client.post(
            "/api/sandbox/reset", json={"confirm": "RESET_SYNTHETIC_DATA"}, headers=HEADERS
        ).status_code
        == 200
    )


def test_untrusted_web_origin_and_simple_posts_are_rejected(client):
    body = {"request": "Read FILE-001"}
    assert client.post("/api/tasks", json=body).status_code == 403
    assert (
        client.post(
            "/api/tasks", json=body, headers={**HEADERS, "Origin": "https://attacker.example"}
        ).status_code
        == 403
    )
    assert client.get("/api/health", headers={"Host": "attacker.example"}).status_code == 400
    assert client.get("/api/summary").json()["tasks"] == 0
