from pydantic import BaseModel
from typing import Optional

class MaterialRestockRequest(BaseModel):
    material_id: int  # The ID of the material being restocked
    quantity: float  # The quantity of material to be added to inventory
    note: Optional[str] = None  # An optional note to describe the reason for the restock

    class Config:
        orm_mode = True
