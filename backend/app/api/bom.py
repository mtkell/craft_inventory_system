from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.bom import BoMCreate, BoMRead
from app.crud import bom as crud_bom
from app.models import bom as model_bom
from app.db.database import SessionLocal, engine
from app.utils.bom import calculate_materials_for_batch

model_bom.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/bom", tags=["Bill of Materials"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BoMRead)
def create_bom_entry(bom: BoMCreate, db: Session = Depends(get_db)):
    return crud_bom.create_bom(db, bom)

@router.get("/", response_model=list[BoMRead])
def list_bom_entries(product_id: int | None = Query(default=None), db: Session = Depends(get_db)):
    return crud_bom.get_boms(db, product_id=product_id)

@router.get("/calculate/")
def calculate_materials(
    product_id: int,
    batch_size: int = 1,
    check_availability: bool = False,
    db: Session = Depends(get_db)
):
    return calculate_materials_for_batch(db, product_id, batch_size, check_availability)
