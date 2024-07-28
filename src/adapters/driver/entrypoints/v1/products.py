from typing import Optional
from fastapi import APIRouter

router = APIRouter(prefix="/products")

@router.get("/")
def list_products(category: Optional[str] = None):
  return {"msg": category}

@router.get("/{id}")
async def get_product_by_id(id: int):
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