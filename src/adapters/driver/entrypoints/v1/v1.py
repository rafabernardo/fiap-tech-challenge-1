from fastapi import APIRouter
from src.adapters.driver.entrypoints.v1.register import router as register_router

router = APIRouter()


@router.get("/ping")
async def read_main():
    return {"msg": "pong"}


def create_routes():
    router.include_router(register_router, prefix="/register")
    # app.include_router(settings_router)