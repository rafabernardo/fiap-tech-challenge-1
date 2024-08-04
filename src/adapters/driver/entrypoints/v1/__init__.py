from adapters.driver.entrypoints.v1 import orders, products, users
from fastapi import APIRouter


def get_v1_routers() -> APIRouter:
    router = APIRouter(prefix="/v1")
    router.include_router(users.router, tags=["Users"])
    router.include_router(products.router, tags=["Products"])
    router.include_router(orders.router, tags=["Orders"])
    return router
