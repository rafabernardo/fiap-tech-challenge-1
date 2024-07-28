from fastapi import APIRouter

from adapters.driver.entrypoints.v1 import users, products, orders

 
def get_v1_routers() -> APIRouter:
    router = APIRouter(prefix="/v1")
    router.include_router(users.router, tags=["users"])
    router.include_router(products.router, tags=["products"])
    router.include_router(orders.router, tags=["orders"])
    return router