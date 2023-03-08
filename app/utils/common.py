import tiktoken
import base64

# for a given content string, counts the number of tokens to be billed for
async def count_tokens(payload: str):
    return 0

# determines whether the request would be processed furthur or not
# this includes many check conditions including the max permitted token count
async def determine_request_validity():
    return True

async def base64_encode_string(payload: str):
    byte_encoding = payload.encode("ascii")
    return str(base64.b64encode(byte_encoding))
