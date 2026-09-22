import argparse
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from safeagent.agent.agent import DEMO_REQUESTS, TaskService
from safeagent.bootstrap import bootstrap
from safeagent.sandbox.models import File
from safeagent.sandbox.seed import seed_database


def main() -> None:
    parser = argparse.ArgumentParser(description="SafeAgent synthetic sandbox (foundation release)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="Apply migrations and seed missing synthetic fixtures")
    reset = commands.add_parser("reset", help="Delete local synthetic data and traces, then reseed")
    reset.add_argument("--yes", action="store_true", required=True)
    demo = commands.add_parser("demo", help="Reset synthetic state and run a deterministic demo")
    demo.add_argument("name", choices=list(DEMO_REQUESTS))
    run = commands.add_parser("run", help="Run a constrained mock command without resetting")
    run.add_argument("request")
    commands.add_parser("inspect", help="Inspect synthetic file metadata")
    commands.add_parser("serve", help="Serve the API on loopback port 8000")
    args = parser.parse_args()
    if args.command == "serve":
        import uvicorn

        uvicorn.run("safeagent.main:app", host="127.0.0.1", port=8000)
        return
    gateway = bootstrap()
    try:
        if args.command == "init":
            result = {"status": "initialized"}
        elif args.command == "reset":
            seed_database(gateway.engine, reset=True)
            result = {
                "status": "reset",
                "removed": "Synthetic tasks, execution traces and fixtures",
            }
        elif args.command in {"demo", "run"}:
            if args.command == "demo":
                seed_database(gateway.engine, reset=True)
                request, adversarial = DEMO_REQUESTS[args.name], args.name == "blocked"
            else:
                request, adversarial = args.request, False
            try:
                result = TaskService(gateway).run(request, adversarial=adversarial)
            except ValueError as exc:
                parser.error(str(exc))
        else:
            with Session(gateway.engine) as db:
                result = {
                    "files": [
                        {"id": f.id, "title": f.title, "version": f.version}
                        for f in db.scalars(select(File).order_by(File.id))
                    ]
                }
        print(json.dumps(result, indent=2, default=str))
    finally:
        gateway.engine.dispose()


if __name__ == "__main__":
    main()
