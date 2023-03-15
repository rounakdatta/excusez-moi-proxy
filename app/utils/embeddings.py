import openai
import hashlib
import numpy
from db.db import Database
from utils.common import base64_encode_string, count_embedding_tokens
from config.openai import openai_config
import numpy
from typing import List

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
async def check_if_embeddings_already_generated(db: Database, embedding_id: str):
    return await db.fetch_val("SELECT EXISTS(SELECT 1 FROM embeddings WHERE embedding_id = $1)", embedding_id)

async def get_if_embeddings_already_generated(db: Database, embedding_id: str):
    return await db.fetch_all("SELECT * FROM embeddings WHERE embedding_id = $1", embedding_id)

# utility to break down the complete document into smaller chunks to be batch sent for generating embeddings
# smaller embeddings (think RISC) help reduce the base data while querying as well
async def break_down_document(payload: str, sentence_splitter):
    total_payload_token_count = await count_embedding_tokens(payload)
    n_of_splits = total_payload_token_count // int(openai_config.embedding_model_optimal_input_tokens) + 1

    # we break it heuristically by text, so token count for each piece wouldn't be equal
    individual_sentences = sentence_splitter.split([payload])[0]
    individual_sentences = [str(el) for el in individual_sentences]
    collection_of_inputs = numpy.array_split(individual_sentences, n_of_splits)
    return [". ".join(list(el)) for el in collection_of_inputs]

# calls external OpenAI API to generate the embeddings array, returned as numpy array
async def generate_embeddings_external(payload):
    print(payload)
    external_response = openai.Embedding.create(model=openai_config.embedding_model_name, input=payload)
    # TODO: make sure to store usage details into database
    return [numpy.array(el["embedding"]) for el in external_response["data"]]

# persists embedding to persistent storage so that it can be re-used
async def persist_embeddings_to_storage(db: Database, embeddings: List[numpy.ndarray], raw_collection: List[str], url: str, embedding_id: str, content_type: str):
    embedding_data_rows = []
    
    for i in range(len(raw_collection)):
        embedding_data = {
            "embedding": embeddings[i],
            "raw_payload": await base64_encode_string(raw_collection[i]),
            "anchor_url": await base64_encode_string(url),
            "embedding_id": embedding_id,
            "content_type": content_type
        }
        embedding_data_row = tuple(embedding_data.values())
        embedding_data_rows.append(embedding_data_row)

    await db.execute_with_vector_registered("INSERT INTO embeddings (embedding, encoded_raw_payload, anchor_url, embedding_id, content_type) VALUES ($1, $2, $3, $4, $5)", embedding_data_rows)
    return

async def search_nearest_embeddings(db: Database, search_query_embeddings: numpy.ndarray, url: str):
    anchor_url = await base64_encode_string(url)
    search_results = await db.fetch_all("SELECT embedding_id, encoded_raw_payload FROM embeddings WHERE anchor_url = $1 AND content_type = 'd' ORDER by embedding <-> $2 LIMIT 10", anchor_url, search_query_embeddings)
    return search_results
