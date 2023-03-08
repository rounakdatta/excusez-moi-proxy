import fastapi
from api.models.embeddings import EmbeddingRequest
from db.db import Database, get_db_conn
from config.openai import get_openai_configured
import utils.embeddings as emb

router = fastapi.APIRouter()
get_openai_configured()

# this endpoint is called once to generate the embeddings for the particular textual content
# we check the cache first, and if doesn't exist then only make a remote call to OpenAI
@router.post("/embeddings")
async def generate_embeddings(request: EmbeddingRequest, db: Database = fastapi.Depends(get_db_conn)):
    emb_id = await emb.generate_id_for_embedding(request.url, request.content)
    await emb.persist_embeddings_to_storage(
        db,
        await emb.generate_embeddings_external(request.content),
        request.content,
        emb_id
    )

    # we return OK to denote that the embedding is now ready to be used
    return fastapi.Response(content="OK", status_code=200)

# this endpoint checks in the cache whether the embedding is present or not
@router.get("/embeddings/{embedding_id}/status")
async def get_embeddings_status(embedding_id: str, db: Database = fastapi.Depends(get_db_conn)):
    # we return OK denoting that the embedding has been found in the cache
    return fastapi.Response(content="OK", status_code=200)
