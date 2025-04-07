from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

def get_products(db: Session, skip: int = 0, limit: int = 100, location_id: int | None = None):
    query = db.query(Product)
    if location_id is not None:
        query = query.filter(Product.location_id == location_id)
    return query.offset(skip).limit(limit).all()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
