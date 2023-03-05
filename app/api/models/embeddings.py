import pydantic

# this will be used to request embedding generation for a given URL and its content
class EmbeddingRequest(pydantic.BaseModel):
    url: str
    content: str
