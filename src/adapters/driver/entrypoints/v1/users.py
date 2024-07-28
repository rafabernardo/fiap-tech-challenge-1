from fastapi import APIRouter

router = APIRouter(prefix="/users")

@router.get("")
async def list_users():
  return {"msg": "pong"}

@router.get("/{id}")
async def get_user_by_id(id: int):
  return {"msg": id}

@router.get("/cpf/{cpf}")
async def get_user_by_cpf(cpf: str):
  return {"msg": cpf}

@router.post("/register")
async def register():
  return {"msg":"pong"}

@router.delete("/delete/{id}")
async def delete(id: int):
  return {"msg":id}

@router.patch("/{id}")
async def update(id: int):
  return {"msg":id}