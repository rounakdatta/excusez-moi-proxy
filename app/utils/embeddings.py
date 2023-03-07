import openai

# generate the unique id for the embedding for this URL
# this function should be absolutely deterministic for exactly same `content`
# the content should ideally be cleaned in a standardized way, and url should be stripped of any unnecessary parameters
async def generate_id_for_embedding(url: str, payload: str):
    return ""

# check in the cache whether the embeddings for this id has already been generated
# if exists, fetch it
async def get_if_embeddings_already_generated(embedding_id: str):
    return {}

# calls external OpenAI API to generate the embeddings array
async def generate_embeddings_external(payload: str):
    return {}

# caches the embedding to persistent storage so that it can be re-used
async def cache_embeddings_to_storage(embedding_id: str, embeddings: dict):
    return
