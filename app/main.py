import fastapi
from api.endpoints import health, preparation, search
from db.db import Database, get_db_conn

API_PREFIX = "/api/v1"
app = fastapi.FastAPI()

app.include_router(health.router, prefix=API_PREFIX)
app.include_router(preparation.router, prefix=API_PREFIX)
app.include_router(search.router, prefix=API_PREFIX)

db = get_db_conn()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
