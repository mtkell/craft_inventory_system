from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductRead
from app.crud import product as crud_product
from app.models import product as model_product
from app.db.database import SessionLocal, engine

model_product.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db=db, product=product)

@router.get("/", response_model=list[ProductRead])
def read_products(
    skip: int = 0,
    limit: int = 100,
    location_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return crud_product.get_products(db, skip=skip, limit=limit, location_id=location_id)

