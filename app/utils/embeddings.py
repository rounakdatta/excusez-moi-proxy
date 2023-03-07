import openai
import hashlib
from db.db import Database

EMBEDDING_MODEL = "text-embedding-ada-002"

# generate the unique id for the embedding for this URL
# this function should be absolutely deterministic for exactly same `content`
# the content should ideally be cleaned in a standardized way, and url should be stripped of any unnecessary parameters
async def generate_id_for_embedding(url: str, payload: str):
    # generate SHA256 digest for the url
    urlSha = hashlib.sha256(url.encode('utf-8'))
    urlShaDigest = urlSha.hexdigest()[:5]

    # generate SHA256 digest for the payload
    payloadSha = hashlib.sha256(payload.encode('utf-8'))
    payloadShaDigest = payloadSha.hexdigest()[:10]

    # embedding id the combination of the two, separated by colon
    return ":".join([urlShaDigest, payloadShaDigest])

# check in the cache whether the embeddings for this id has already been generated
# if exists, fetch it
async def get_if_embeddings_already_generated(embedding_id: str):
    return {}

# calls external OpenAI API to generate the embeddings array
async def generate_embeddings_external(payload: str) -> list[float]:
    external_response = openai.Embedding.create(model=EMBEDDING_MODEL, input=payload)
    # TODO: make sure to store usage details into database
    return external_response["data"][0]["embedding"]

# persists embedding to persistent storage so that it can be re-used
async def persist_embeddings_to_storage(db: Database, embeddings: list[float], raw_payload: str, embedding_id: str):
    # TODO: base64 encode the raw payloads
    await db.execute("INSERT INTO embeddings (embedding, encoded_raw_payload, embedding_id) VALUES ($1, $2, $3)", embeddings, "REPLACE_ME", embedding_id)
    return
