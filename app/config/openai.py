import os
import openai

class OpenAIConfig:
    org = os.getenv("OPENAI_ORGANIZATION")
    api_key = os.getenv("OPENAI_API_KEY")

    # OpenAI's second generation model returns embeddings of upto 1536 dimensions
    # https://platform.openai.com/docs/guides/embeddings/second-generation-models
    embedding_max_dimensions = 1536

    # model names to be used
    embedding_model_name = "text-embedding-ada-002"

openai_config = OpenAIConfig()

def get_openai_configured():
    openai.organization = openai_config.org
    openai.api_key = openai_config.api_key
