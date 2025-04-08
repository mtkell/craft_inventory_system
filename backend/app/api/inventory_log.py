from fastapi import APIRouter, Depends, Query, HTTPException
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

@router.get("/inventory/", response_model=list[InventoryLogRead], tags=["Inventory Logs"])
def get_inventory_logs(
    db: Session = Depends(get_db),
    material_id: Optional[int] = None,
    type: Optional[Literal["restock", "deduction"]] = None,
    limit: int = Query(100, le=500)
):
    """
    Retrieve inventory change logs.

    - You can filter logs by **material_id** to get logs for a specific material.
    - You can filter by **type** to retrieve either **restock** or **deduction** logs.
    - The **limit** parameter controls how many logs are returned, with a default of 100 (max 500).

    **Example Request**:
    ```json
    {
        "material_id": 1,
        "type": "deduction",
        "limit": 50
    }
    ```

    **Example Response**:
    ```json
    [
        {
            "id": 1,
            "material_id": 1,
            "change_type": "deduction",
            "quantity": 10,
            "remaining": 50,
            "timestamp": "2025-04-05T12:00:00",
            "note": "Auto deduction for batch of size 10"
        },
        {
            "id": 2,
            "material_id": 1,
            "change_type": "restock",
            "quantity": 20,
            "remaining": 70,
            "timestamp": "2025-04-06T12:00:00",
            "note": "Restocked 20 units"
        }
    ]
    ```

    - **Error Response** (Invalid Query):
    ```json
    {
        "detail": "Invalid type. Expected 'restock' or 'deduction'."
    }
    ```
    """
    query = db.query(InventoryChangeLog)

    if material_id is not None:
        query = query.filter(InventoryChangeLog.material_id == material_id)

    if type is not None:
        if type not in ["restock", "deduction"]:
            raise HTTPException(status_code=400, detail="Invalid type. Expected 'restock' or 'deduction'.")
        query = query.filter(InventoryChangeLog.change_type == type)

    return query.order_by(InventoryChangeLog.timestamp.desc()).limit(limit).all()
