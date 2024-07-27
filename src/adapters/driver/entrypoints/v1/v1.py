from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def read_main():
    return {"msg": "pong"}
