from alembic import context

from safeagent.sandbox.database import create_database
from safeagent.sandbox.models import Base
from safeagent.settings import Settings

config = context.config


def run(connection):
    context.configure(connection=connection, target_metadata=Base.metadata, render_as_batch=True)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    context.configure(
        url=Settings().database_url, target_metadata=Base.metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()
elif config.attributes.get("connection") is not None:
    run(config.attributes["connection"])
else:
    engine = create_database(Settings().database_url)
    with engine.connect() as connection:
        run(connection)
    engine.dispose()
