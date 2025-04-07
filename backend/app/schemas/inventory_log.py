from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class InventoryLogRead(BaseModel):
    id: int
    material_id: int
    change_type: Literal["restock", "deduction"]
    quantity: float
    remaining: float
    note: str | None
    timestamp: datetime

    class Config:
        orm_mode = True
