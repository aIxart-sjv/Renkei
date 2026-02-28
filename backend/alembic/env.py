import sys
import os

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


# =========================
# ADD PROJECT ROOT TO PATH
# =========================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# =========================
# IMPORT CONFIG
# =========================

from app.db.base import Base
from app.config import settings


# =========================
# ALEMBIC CONFIG
# =========================

config = context.config


# =========================
# SET DATABASE URL
# =========================

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL
)


# =========================
# LOGGING
# =========================

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# =========================
# TARGET METADATA
# =========================

target_metadata = Base.metadata


# =========================
# OFFLINE MIGRATIONS
# =========================

def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# =========================
# ONLINE MIGRATIONS
# =========================

def run_migrations_online():
    """
    Run migrations in 'online' mode.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )


    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )


        with context.begin_transaction():
            context.run_migrations()


# =========================
# EXECUTE
# =========================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()