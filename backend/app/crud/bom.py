from sqlalchemy.orm import Session
from app.models.bom import BillOfMaterial
from app.schemas.bom import BoMCreate

def get_boms(db: Session, product_id: int | None = None):
    query = db.query(BillOfMaterial)
    if product_id is not None:
        query = query.filter(BillOfMaterial.product_id == product_id)
    return query.all()

def create_bom(db: Session, bom: BoMCreate):
    db_bom = BillOfMaterial(**bom.dict())
    db.add(db_bom)
    db.commit()
    db.refresh(db_bom)
    return db_bom
