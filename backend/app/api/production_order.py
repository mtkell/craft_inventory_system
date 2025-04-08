from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.production_order import ProductionOrder, ProductionStatus
from app.schemas.production_order import ProductionOrderCreate, ProductionOrderRead
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from typing import List
from datetime import datetime

router = APIRouter(prefix="/production_orders", tags=["Production Orders", "Order Management"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductionOrderRead, tags=["Production Orders", "Order Management"])
def create_order(
    data: ProductionOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
    """
    Create a new production order.

    - **admin** and **operator** roles can create orders.
    - The new order will be marked as **PLANNED** by default.

    **Example Request**:
    ```json
    {
        "product_id": 1,
        "batch_size": 100,
        "note": "Start production for batch 100"
    }
    ```

    **Example Response**:
    ```json
    {
        "id": 1,
        "product_id": 1,
        "batch_size": 100,
        "note": "Start production for batch 100",
        "status": "PLANNED",
        "created_at": "2025-04-05T12:00:00",
        "completed_at": null
    }
    ```
    """
    order = ProductionOrder(
        product_id=data.product_id,
        batch_size=data.batch_size,
        note=data.note,
        status=ProductionStatus.PLANNED
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=List[ProductionOrderRead], tags=["Production Orders", "Order Management"])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
    """
    Retrieve a list of all production orders.
    
    - **admin** and **operator** roles can access this endpoint.
    - Orders are returned sorted by **created_at** in descending order.

    **Example Response**:
    ```json
    [
        {
            "id": 1,
            "product_id": 1,
            "batch_size": 100,
            "note": "Start production for batch 100",
            "status": "PLANNED",
            "created_at": "2025-04-05T12:00:00",
            "completed_at": null
        },
        {
            "id": 2,
            "product_id": 2,
            "batch_size": 50,
            "note": "Start production for batch 50",
            "status": "PLANNED",
            "created_at": "2025-04-06T12:00:00",
            "completed_at": null
        }
    ]
    ```
    """
    return db.query(ProductionOrder).order_by(ProductionOrder.created_at.desc()).all()

@router.get("/{order_id}", response_model=ProductionOrderRead, tags=["Production Orders", "Order Management"])
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
    """
    Get the details of a specific production order by its ID.

    - **admin** and **operator** roles can access this endpoint.

    **Example Response**:
    ```json
    {
        "id": 1,
        "product_id": 1,
        "batch_size": 100,
        "note": "Start production for batch 100",
        "status": "PLANNED",
        "created_at": "2025-04-05T12:00:00",
        "completed_at": null
    }
    ```
    """
    order = db.query(ProductionOrder).filter(ProductionOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production order not found")
    return order

@router.delete("/{order_id}", tags=["Production Orders", "Order Management"])
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Delete a specific production order by its ID.

    - **admin** role can delete orders.

    **Example Response**:
    ```json
    {
        "status": "success",
        "message": "Production order 1 deleted"
    }
    ```
    """
    order = db.query(ProductionOrder).filter(ProductionOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production order not found")
    db.delete(order)
    db.commit()
    return {"status": "success", "message": f"Production order {order_id} deleted"}

@router.put("/{order_id}/status", response_model=ProductionOrderRead, tags=["Production Orders", "Order Management"])
def update_status(
    order_id: int,
    status: ProductionStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
    """
    Update the status of a production order.

    - **admin** and **operator** roles can update the status.
    - When the status is set to **COMPLETE**, the `completed_at` field is updated to the current time.

    **Example Request**:
    ```json
    {
        "status": "COMPLETE"
    }
    ```

    **Example Response**:
    ```json
    {
        "id": 1,
        "product_id": 1,
        "batch_size": 100,
        "note": "Start production for batch 100",
        "status": "COMPLETE",
        "created_at": "2025-04-05T12:00:00",
        "completed_at": "2025-04-05T14:00:00"
    }
    ```
    """
    order = db.query(ProductionOrder).filter(ProductionOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production order not found")
    order.status = status
    if status == ProductionStatus.COMPLETE:
        order.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    return order
