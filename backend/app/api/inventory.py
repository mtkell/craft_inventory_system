from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from app.models.user import User

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/")
async def read_inventory(current_user: User = Depends(get_current_user)):
    return {"message": f"Inventory API is working for {current_user.username}"}
