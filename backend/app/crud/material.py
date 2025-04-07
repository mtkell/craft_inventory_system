from sqlalchemy.orm import Session
from app.models.material import Material
from app.schemas.material import MaterialCreate

def get_materials(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Material).offset(skip).limit(limit).all()

def create_material(db: Session, material: MaterialCreate):
    db_material = Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material
