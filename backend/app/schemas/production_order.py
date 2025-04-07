from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class ProductionOrderCreate(BaseModel):
    product_id: int
    batch_size: int
    note: Optional[str] = None

class ProductionOrderRead(BaseModel):
    id: int
    product_id: int
    batch_size: int
    status: Literal["planned", "in_progress", "complete"]
    note: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True
