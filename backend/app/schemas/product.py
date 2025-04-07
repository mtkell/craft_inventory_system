from pydantic import BaseModel
from app.schemas.location import LocationRead

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    quantity: int = 0
    price: float = 0.0
    location_id: int | None = None

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    location: LocationRead | None = None

    class Config:
        orm_mode = True
