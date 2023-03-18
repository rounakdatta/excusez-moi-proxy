import fastapi
from api.models.embeddings import EmbeddingRequest
from db.db import Database, get_db_conn
from config.openai import get_openai_configured
from config.text_split import get_embedding_text_splitter
import utils.embeddings as emb

router = fastapi.APIRouter()
get_openai_configured()
sentence_splitter = get_embedding_text_splitter()


@router.post("/prepare")
async def prepare_base_document(request: EmbeddingRequest, db: Database = fastapi.Depends(get_db_conn)):
    await generate_embeddings(request, db)

    # we return OK to denote that the embedding is now ready to be used
    return fastapi.Response(content="OK", status_code=200)


async def generate_embeddings(request: EmbeddingRequest, db: Database):
    """
    This function coordinates the generation of embeddings. If the embeddings were already generated previously, we use them.
    """
    emb_id = await emb.generate_id_for_embedding(request.url, request.content)
    does_already_exist = await emb.check_if_embeddings_already_generated(db, emb_id)

    if not does_already_exist:
        collection_of_documents = await emb.break_down_document(request.content, sentence_splitter)
        collection_of_embeddings = await emb.generate_embeddings_external(collection_of_documents)

        await emb.persist_embeddings_to_storage(
            db,
            collection_of_embeddings,
            collection_of_documents,
            request.url,
            emb_id,
            "d"  # to indicate document embedding
        )
