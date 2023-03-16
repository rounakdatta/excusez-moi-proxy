import fastapi

router = fastapi.APIRouter()


@router.get("/health")
async def get_health():
    return fastapi.Response(content="OK", status_code=200)
