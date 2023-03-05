from fastapi import APIRouter, Response

router = APIRouter()

@router.get("/health")
async def get_health():
    return Response(content="OK", status_code=200)
