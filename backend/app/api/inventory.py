from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/inventory", tags=["Inventory", "Inventory Management"])

@router.get("/", tags=["Inventory", "Inventory Management"])
async def read_inventory(current_user: User = Depends(get_current_user)):
    """
    Retrieve inventory details.

    - **admin** and **operator** roles can access this endpoint.
    """
    return {"message": f"Inventory API is working for {current_user.username}"}
