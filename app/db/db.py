import asyncpg
from asyncpg.pool import Pool
from config.db import db_config
from pgvector.asyncpg import register_vector

class Database:
    def __init__(self, url: str):
        self.url = url
        self.pool: Pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.url)

    async def disconnect(self):
        if self.pool is not None:
            self.pool.close()
            await self.pool.wait_closed()

    async def fetch_one(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def fetch_val(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchval(query, *args)

    async def fetch_all(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def execute_with_vector_registered(self, query: str, *args):
        async with self.pool.acquire() as connection:
            await register_vector(connection)
            return await connection.execute(query, *args)

# intialize the database connections
db_conn = Database(db_config.db_config_urn)

def get_db_conn():
    return db_conn
