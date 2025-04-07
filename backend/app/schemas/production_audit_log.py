from pydantic import BaseModel
from datetime import datetime

class ProductionAuditLogRead(BaseModel):
    id: int
    production_order_id: int
    action: str
    note: str | None
    timestamp: datetime

    class Config:
        orm_mode = True
