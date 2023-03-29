import openai
import hashlib
import numpy
from db.db import Database
from utils.common import base64_encode_string, base64_decode_string, count_embedding_tokens
from config.openai import openai_config
import json


async def find_answer_to_question(nearest_embeddings: list, search_query: str, sentence_splitter):
    """
    Seek the answer given the nearest embeddings (context) and the search query.
    This also decides whether to make a single or multiple chat completion calls.
    """
    nearest_text_sections = [await base64_decode_string(e["encoded_raw_payload"]) for e in nearest_embeddings]
    prompt = ". ".join(nearest_text_sections)

    chat_completion_responses = []

    # if the entire search payload fits within a single query then we go all in
    total_token_count = await count_embedding_tokens(prompt)
    if total_token_count <= openai_config.completion_model_optimal_input_tokens:
        chat_completion_responses = [await generate_chat_completion_external(prompt, search_query)]
    else:
        # else we bank on multiple API calls
        collection_of_calls = sentence_splitter.split_text(prompt)

        print("total number of calls: ", len(collection_of_calls))
        chat_completion_responses = [await generate_chat_completion_external(call, search_query) for call in collection_of_calls]

    answers = []
    for response in chat_completion_responses:
        try:
            deserAnswer = json.loads(response['choices'][0]['message']['content'])
            answers.append(deserAnswer)
        except:
            print("Malformed message:")
            print(response['choices'][0]['message']['content'])
            continue

    return {"answers": answers}


async def generate_chat_completion_external(chat_text: str, search_query: str):
    """
    Use external API (OpenAI) to generate the chat completions for a given chat context and a search.
    Contains all the prompt engineering techniques to receive structured answers.
    """
    # try:
    searchResponse = openai.ChatCompletion.create(
        model=openai_config.completion_model_name,
        temperature=0,
        messages=[
            # later introduce system dialogues for better framing
            {"role": "user", "content": 'Answer exactly the matching term, absolutely nothing else. Your answer should be strictly a valid JSON {"resp": "<answer>"}. If there is no definite answer, just say {"resp": "KZZ"}'},
            {"role": "assistant", "content": '{"resp": "KZZ"}'},
            {"role": "user", "content": chat_text + ". " + search_query}
        ]
    )

    return searchResponse
