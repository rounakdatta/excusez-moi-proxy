import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import create_engine
from pgvector.asyncpg import register_vector
import asyncpg
import os

from alembic import context
from app.db.models import Base, User

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    url = "postgresql+asyncpg://{user}:{password}@{host}/{database}".format(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"]
    )
    connectable = AsyncEngine(create_engine(url))

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()
    await set_up_vector_migration()

# additional setup to get custom vector datatype working
async def set_up_vector_migration():
    url = "postgresql://{user}:{password}@{host}/{database}".format(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"]
    )
    conn = await asyncpg.connect(
        dsn=url
    )

    # register the vector datatype against the database migrations to be used by albemic
    await register_vector(conn)
    await conn.close()


asyncio.run(run_migrations_online())
