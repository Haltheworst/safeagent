from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.pool import StaticPool


def create_database(url: str) -> Engine:
    parsed = make_url(url)
    if parsed.get_backend_name() != "sqlite":
        raise ValueError("This release supports only the local SQLite sandbox.")
    if parsed.database and parsed.database != ":memory:":
        Path(parsed.database).parent.mkdir(parents=True, exist_ok=True)
    options = {"poolclass": StaticPool} if parsed.database in (None, "", ":memory:") else {}
    engine = create_engine(url, connect_args={"check_same_thread": False}, **options)

    @event.listens_for(engine, "connect")
    def configure_connection(connection, _record):
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=5000")

    return engine
