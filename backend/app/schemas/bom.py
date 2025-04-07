from pydantic import BaseModel
from app.schemas.product import ProductRead
from app.schemas.material import MaterialRead

class BoMBase(BaseModel):
    product_id: int
    material_id: int
    quantity: float

class BoMCreate(BoMBase):
    pass

class BoMRead(BoMBase):
    id: int
    product: ProductRead | None = None
    material: MaterialRead | None = None

    class Config:
        orm_mode = True
