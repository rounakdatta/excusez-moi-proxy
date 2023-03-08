import fastapi
from api.models.embeddings import EmbeddingRequest
from db.db import Database, get_db_conn
from config.openai import get_openai_configured
import utils.embeddings as emb
import utils.completions as comp

router = fastapi.APIRouter()
get_openai_configured()

# this endpoint will (1) first generate the embeddings for the search query
# (2) similarity-match with the existing embeddings for the entire document
# (3) use OpenAI completions API to generate an answer
@router.post("/answer")
async def answer_question(request: EmbeddingRequest, db: Database = fastapi.Depends(get_db_conn)):
    search_query_embeddings = await generate_embeddings_and_return(request, db)
    nearest_sections = await emb.search_nearest_embeddings(db, search_query_embeddings, request.url)

    response = await comp.find_answer_to_question(nearest_sections, request.content)
    answer = response['choices'][0]['message']['content']

    # we return OK to denote that the embedding is now ready to be used
    return fastapi.Response(content=str(answer), status_code=200)

async def generate_embeddings_and_return(request: EmbeddingRequest, db: Database):
    emb_id = await emb.generate_id_for_embedding(request.url, request.content)
    existing_embeddings = await emb.get_if_embeddings_already_generated(db, emb_id)
    if existing_embeddings is not None:
        return existing_embeddings['embedding']

    generated_embeddings = await emb.generate_embeddings_external(request.content)
    await emb.persist_embeddings_to_storage(
        db,
        generated_embeddings,
        request.content,
        request.url,
        emb_id,
        "q" # to indicate query embedding
    )

    return generated_embeddings
