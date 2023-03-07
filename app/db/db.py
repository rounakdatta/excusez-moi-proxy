import asyncpg
from asyncpg.pool import Pool

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

    async def fetch_all(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)
