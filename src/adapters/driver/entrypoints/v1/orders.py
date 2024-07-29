from typing import Optional
from fastapi import APIRouter

router = APIRouter(prefix="/orders")

@router.get("/")
def list_orders(status: Optional[str] = None):
  return {"msg": status}

@router.get("/{id}")
async def get_order_by_id(id: int):
  return {"msg": id}

@router.post("/register")
async def register():
  return {"msg":"pong"}

@router.delete("/delete/{id}")
async def delete(id: int):
  return {"msg":id}

@router.patch("/{id}")
async def update(id: int):
  return {"msg":id}

@router.post("/checkout")
async def checkout(id: int):
  return {"msg":id}