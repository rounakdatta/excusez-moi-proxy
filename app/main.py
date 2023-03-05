from fastapi import FastAPI
from api.endpoints import health

API_PREFIX = "/api/v1"
app = FastAPI()

app.include_router(health.router, prefix=API_PREFIX)
