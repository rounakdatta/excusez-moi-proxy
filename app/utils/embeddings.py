# generate the unique id for the embedding for this URL
# this function should be absolutely deterministic for exactly same `content`
# the content should ideally be cleaned in a standardized way, and url should be stripped of any unnecessary parameters
async def generate_id_for_embedding(url: str, content: str):
    return ""

# check in the cache whether the embeddings for this id has already been generated
async def check_if_embeddings_already_generated(embedding_id: str):
    return {}
