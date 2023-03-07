import fastapi
from api.endpoints import health, embeddings
from config.db import DatabaseConfig
from db.db import Database

API_PREFIX = "/api/v1"
app = fastapi.FastAPI()

# intialize the database connections
db_config = DatabaseConfig()
db = Database(url)

app.include_router(health.router, prefix=API_PREFIX)
app.include_router(embeddings.router, prefix=API_PREFIX)

# we'll make sure to connect/disconnect from the database gracefully
@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
