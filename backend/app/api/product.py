from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductRead
from app.crud import product as crud_product
from app.models import product as model_product
from app.db.database import SessionLocal, engine

model_product.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/products", tags=["Products", "Inventory Management"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductRead, tags=["Products", "Inventory Management"])
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new product entry.

    - **admin** role required to create products.
    - The new product will be added to the inventory with a default stock.
    """
    return crud_product.create_product(db=db, product=product)

@router.get("/", response_model=list[ProductRead], tags=["Products", "Inventory Management"])
def read_products(
    skip: int = 0,
    limit: int = 100,
    location_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of products.

    - **admin** and **operator** roles can view the products.
    - Allows for filtering products by location (if a location ID is provided).

    - **Example**:
      - `GET /products?skip=0&limit=10&location_id=2`
    """
    return crud_product.get_products(db, skip=skip, limit=limit, location_id=location_id)
