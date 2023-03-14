import openai
import hashlib
import numpy
from db.db import Database
from utils.common import base64_encode_string, base64_decode_string, count_embedding_tokens
from config.openai import openai_config

async def find_answer_to_question(nearest_embeddings: list, search_query: str):
    nearest_text_sections = [await base64_decode_string(e["encoded_raw_payload"]) for e in nearest_embeddings]
    prompt = ". ".join(nearest_text_sections)

    # if the entire search payload fits within a single query then we go all in
    total_token_count = await count_embedding_tokens(prompt)
    if total_token_count <= openai_config.completion_model_optimal_input_tokens:
        singular_response = await generate_chat_completion_external(prompt, search_query)
        return [singular_response]

    # else we bank on multiple API calls
    n_of_splits = total_token_count // openai_config.completion_model_optimal_input_tokens
    collection_of_calls = numpy.array_split(nearest_text_sections, n_of_splits)
    collection_of_calls = [". ".join(list(el)) for el in collection_of_calls]

    chat_completion_responses = [await generate_chat_completion_external(call, search_query)['choices'][0]['message']['content'] for call in collection_of_calls]
    return {"answers": chat_completion_responses}

async def generate_chat_completion_external(chat_text: str, search_query: str):
    searchResponse = openai.ChatCompletion.create(
        model=openai_config.completion_model_name,
        temperature=0,
        messages=[
            # later introduce system dialogues for better framing
            {"role": "user", "content": 'Answer exactly the matching term, absolutely nothing else. Your answer should be in the form of a valid JSON {"resp": "<answer>"}. If there is no answer, just say OK'},
            {"role": "assistant", "content": '{"resp": "OK"}'},
            {"role": "user", "content": chat_text + ". " + search_query}
        ]
    )

    return searchResponse
