from pydantic import BaseModel

class MaterialBase(BaseModel):
    name: str
    description: str | None = None
    quantity: float = 0.0
    unit: str = "yards"

class MaterialCreate(MaterialBase):
    pass

class MaterialRead(MaterialBase):
    id: int

    class Config:
        orm_mode = True
