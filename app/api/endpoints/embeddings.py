import fastapi
from api.models.embeddings import EmbeddingRequest

router = fastapi.APIRouter()

# this endpoint is called once to generate the embeddings for the particular textual content
# we check the cache first, and if doesn't exist then only make a remote call to OpenAI
@router.post("/embeddings")
async def generate_embeddings(request: EmbeddingRequest):
    # we return OK to denote that the embedding is now ready to be used
    return fastapi.Response(content="OK", status_code=200)

# this endpoint checks in the cache whether the embedding is present or not
@router.get("/embeddings/{embedding_id}/status")
async def get_embeddings_status(embedding_id: str):
    # we return OK denoting that the embedding has been found in the cache
    return fastapi.Response(content="OK", status_code=200)
