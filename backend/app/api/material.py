from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.material import MaterialCreate, MaterialRead
from app.crud import material as crud_material
from app.models import material as model_material
from app.db.database import SessionLocal, engine
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles

model_material.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/materials", tags=["Materials", "Inventory Management"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MaterialRead, tags=["Materials", "Inventory Management"])
def create_material(
    material: MaterialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
    """
    Create a new material entry.

    - **admin** and **operator** roles can create materials.
    """
    return crud_material.create_material(db=db, material=material)

@router.get("/", response_model=list[MaterialRead], tags=["Materials", "Inventory Management"])
def read_materials(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
    """
    Retrieve a list of materials.

    - **admin** and **operator** roles can access this endpoint.
    """
    return crud_material.get_materials(db, skip=skip, limit=limit)
