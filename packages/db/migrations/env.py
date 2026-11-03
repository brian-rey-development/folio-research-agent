import os

from alembic import context
from folio_db.migration_filters import include_name
from folio_db.tables import metadata
from sqlalchemy import create_engine

DATABASE_URL_VAR = "DATABASE_URL"


def database_url() -> str:
    url = os.environ.get(DATABASE_URL_VAR)
    if not url:
        raise RuntimeError(f"{DATABASE_URL_VAR} is not set")
    return url


def run_migrations_offline() -> None:
    context.configure(
        url=database_url(),
        target_metadata=metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_name=include_name,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(database_url())
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=metadata,
            include_name=include_name,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
