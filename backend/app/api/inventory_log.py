from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.inventory_log import InventoryChangeLog
from app.schemas.inventory_log import InventoryLogRead
from typing import Optional, Literal

router = APIRouter(prefix="/logs", tags=["Inventory Logs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/inventory/", response_model=list[InventoryLogRead])
def get_inventory_logs(
    db: Session = Depends(get_db),
    material_id: Optional[int] = None,
    type: Optional[Literal["restock", "deduction"]] = None,
    limit: int = Query(100, le=500)
):
    query = db.query(InventoryChangeLog)

    if material_id is not None:
        query = query.filter(InventoryChangeLog.material_id == material_id)

    if type is not None:
        query = query.filter(InventoryChangeLog.change_type == type)

    return query.order_by(InventoryChangeLog.timestamp.desc()).limit(limit).all()
