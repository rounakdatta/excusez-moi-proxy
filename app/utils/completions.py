import openai
import hashlib
import numpy
from db.db import Database
from utils.common import base64_encode_string, base64_decode_string
from config.openai import openai_config

async def find_answer_to_question(nearest_embeddings: list, searchQuery: str):
    nearest_text_sections = [await base64_decode_string(e["encoded_raw_payload"]) for e in nearest_embeddings]
    prompt = ". ".join(nearest_text_sections)
    searchResponse = openai.ChatCompletion.create(
        model=openai_config.completion_model_name,
        temperature=0,
        messages=[
            # later introduce system dialogues for better framing
            {"role": "user", "content": "You will do reading comprehension. Answer exactly as asked, don't provide extra information."},
            {"role": "assistant", "content": "Okay."},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "Okay, I've understood everything you just told."},
            {"role": "user", "content": searchQuery}
        ]
    )

    return searchResponse
