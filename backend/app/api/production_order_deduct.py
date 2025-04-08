from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.production_order import ProductionOrder
from app.schemas.production_order import ProductionOrderRead
from app.services.production_deduction import deduct_for_production_order
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles

router = APIRouter(prefix="/production_orders", tags=["Production Orders", "Material Deduction"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{order_id}/deduct/", response_model=ProductionOrderRead, tags=["Production Orders", "Material Deduction"])
def deduct_materials_for_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
    """
    Deduct materials for a specific production order.

    - **admin** and **operator** roles can deduct materials for an order.
    - This will update the inventory and the production order status.
    
    **Example Request**:
    ```json
    {
        "order_id": 1
    }
    ```

    **Example Response**:
    ```json
    {
        "id": 1,
        "product_id": 1,
        "batch_size": 100,
        "note": "Start production for batch 100",
        "status": "IN_PROGRESS",
        "created_at": "2025-04-05T12:00:00",
        "completed_at": null
    }
    ```
    """
    order = db.query(ProductionOrder).filter(ProductionOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production order not found")

    deduct_for_production_order(order, db)
    db.refresh(order)
    return order
