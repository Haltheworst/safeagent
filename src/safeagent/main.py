from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.middleware.trustedhost import TrustedHostMiddleware

from safeagent.agent.agent import DEMO_REQUESTS, TaskService
from safeagent.bootstrap import bootstrap
from safeagent.runtime.schemas import StrictModel
from safeagent.sandbox.models import AuditEvent, Execution, File, Task
from safeagent.sandbox.seed import FIXTURE_VERSION, seed_database
from safeagent.sandbox.tools import REGISTRY
from safeagent.settings import Settings


class TaskRequest(StrictModel):
    request: str = Field(min_length=1, max_length=500)


class DemoRequest(StrictModel):
    name: Literal["authorized", "blocked", "read"]


class ResetRequest(StrictModel):
    confirm: Literal["RESET_SYNTHETIC_DATA"]


def create_app(settings: Settings | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.gateway = bootstrap(settings)
        yield
        app.state.gateway.engine.dispose()

    app = FastAPI(title="SafeAgent", version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "testserver"]
    )

    @app.middleware("http")
    async def local_ui_boundary(request: Request, call_next):
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            origin = request.headers.get("origin")
            allowed = {
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:8000",
                "http://127.0.0.1:8000",
            }
            if (origin is not None and origin not in allowed) or (
                request.headers.get("x-safeagent-client") != "local-ui"
            ):
                return JSONResponse(
                    {"detail": "Local client header and allowed origin required."}, 403
                )
        return await call_next(request)

    @app.get("/api/health")
    def health():
        return {"status": "ok", "version": "0.1.0", "mode": "deterministic-mock"}

    @app.get("/api/tools")
    def tools():
        return [spec.public_metadata() for spec in REGISTRY.values()]

    @app.post("/api/tasks")
    def run_task(body: TaskRequest):
        try:
            return TaskService(app.state.gateway).run(body.request)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.post("/api/demos")
    def run_demo(body: DemoRequest):
        gateway = app.state.gateway
        with gateway.lock:
            seed_database(gateway.engine, reset=True)
            return TaskService(gateway).run(
                DEMO_REQUESTS[body.name], adversarial=body.name == "blocked"
            )

    @app.post("/api/sandbox/reset")
    def reset(_body: ResetRequest):
        gateway = app.state.gateway
        with gateway.lock:
            seed_database(gateway.engine, reset=True)
        return {"status": "reset", "fixture_version": FIXTURE_VERSION}

    @app.get("/api/sandbox")
    def sandbox():
        # Trusted operator inspection surface. It is never included in the model's tool list.
        with Session(app.state.gateway.engine) as db:
            return {
                "fixture_version": FIXTURE_VERSION,
                "files": [
                    {
                        "id": f.id,
                        "title": f.title,
                        "owner_id": f.owner_id,
                        "sensitivity": f.sensitivity,
                        "version": f.version,
                    }
                    for f in db.scalars(select(File).order_by(File.id))
                ],
            }

    @app.get("/api/tasks")
    def tasks():
        with Session(app.state.gateway.engine) as db:
            return [
                {
                    "task_id": t.id,
                    "request": t.request,
                    "status": t.status,
                    "report": t.report,
                    "created_at": t.created_at,
                }
                for t in db.scalars(select(Task).order_by(Task.created_at.desc()).limit(100))
            ]

    @app.get("/api/tasks/{task_id}/trace")
    def trace(task_id: str):
        with Session(app.state.gateway.engine) as db:
            if db.get(Task, task_id) is None:
                raise HTTPException(404, "Task not found.")
            return [
                {
                    "id": e.id,
                    "task_id": e.task_id,
                    "action_id": e.action_id,
                    "kind": e.kind,
                    "details": e.details,
                    "timestamp": e.timestamp,
                }
                for e in db.scalars(
                    select(AuditEvent).where(AuditEvent.task_id == task_id).order_by(AuditEvent.id)
                )
            ]

    @app.get("/api/summary")
    def summary():
        with Session(app.state.gateway.engine) as db:
            tasks = db.scalars(select(Task)).all()
            executions = db.scalars(select(Execution)).all()
            return {
                "source": "stored_local_tasks_not_research_benchmark",
                "tasks": len(tasks),
                "completed_tasks": sum(t.status == "COMPLETED" for t in tasks),
                "verified_executions": sum(e.verified for e in executions),
                "blocked_proposals": sum(e.state == "BLOCKED" for e in executions),
                "tool_attempts": sum(e.attempts for e in executions),
                "evaluated_tasks": 0,
                "benchmark_status": "NOT_IMPLEMENTED",
            }

    return app


app = create_app()
