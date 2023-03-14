import os
import openai

class OpenAIConfig:
    org = os.getenv("OPENAI_ORGANIZATION")
    api_key = os.getenv("OPENAI_API_KEY")

    # OpenAI's second generation model returns embeddings of upto 1536 dimensions
    # https://platform.openai.com/docs/guides/embeddings/second-generation-models
    embedding_max_dimensions = 1536

    # determines how many tokens are allowed by the embeddings model
    # and how we optimize costs by breaking down inputs
    embedding_model_max_input_tokens = 8192
    embedding_model_optimal_input_tokens = 500

    # determines how many tokens are allowed in total (input+output) by the chat completion model
    completion_model_max_total_tokens = 4096
    completion_model_optimal_input_tokens = 4000

    # model names to be used
    embedding_model_name = "text-embedding-ada-002"
    completion_model_name = "gpt-3.5-turbo"

    # token encoder names
    embedding_token_encoder_name = "cl100k_base"
    completion_token_encoder_name = "cl100k_base"

openai_config = OpenAIConfig()

def get_openai_configured():
    openai.organization = openai_config.org
    openai.api_key = openai_config.api_key
