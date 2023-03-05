import fastapi
from api.endpoints import health, embeddings

API_PREFIX = "/api/v1"
app = fastapi.FastAPI()

app.include_router(health.router, prefix=API_PREFIX)
app.include_router(embeddings.router, prefix=API_PREFIX)
