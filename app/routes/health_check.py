from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["system"])
async def healthcheck():
    return {"status": "ok"}
