from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy.engine import Engine

from safeagent.runtime.gateway import Gateway
from safeagent.runtime.policy import PolicyConfig, PolicyEngine
from safeagent.sandbox.database import create_database
from safeagent.sandbox.seed import seed_database
from safeagent.settings import Settings


def migrate(engine: Engine) -> None:
    # v0.1 runs from a source checkout; migrations/config are repository assets.
    root = Path(__file__).resolve().parents[2]
    config = Config(str(root / "alembic.ini"))
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")


def bootstrap(settings: Settings | None = None) -> Gateway:
    settings = settings or Settings()
    policy = PolicyEngine(PolicyConfig.load(settings.policy_path))
    engine = create_database(settings.database_url)
    migrate(engine)
    seed_database(engine)
    return Gateway(engine, policy)
