from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.material import Material

router = APIRouter(prefix="/materials", tags=["Materials"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/low_stock/")
def get_low_stock_materials(db: Session = Depends(get_db)):
    materials = db.query(Material).filter(Material.quantity < Material.reorder_point).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "quantity": m.quantity,
            "unit": m.unit,
            "reorder_point": m.reorder_point
        }
        for m in materials
    ]
