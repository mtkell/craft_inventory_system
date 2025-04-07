from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.production_order import ProductionOrder, ProductionStatus
from app.schemas.production_order import ProductionOrderCreate, ProductionOrderRead
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from typing import List

router = APIRouter(prefix="/production_orders", tags=["Production Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductionOrderRead)
def create_order(
    data: ProductionOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
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

@router.get("/", response_model=List[ProductionOrderRead])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
    return db.query(ProductionOrder).order_by(ProductionOrder.created_at.desc()).all()

@router.get("/{order_id}", response_model=ProductionOrderRead)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
    order = db.query(ProductionOrder).filter(ProductionOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production order not found")
    return order

@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    order = db.query(ProductionOrder).filter(ProductionOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production order not found")
    db.delete(order)
    db.commit()
    return {"status": "success", "message": f"Production order {order_id} deleted"}

@router.put("/{order_id}/status", response_model=ProductionOrderRead)
def update_status(
    order_id: int,
    status: ProductionStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
    order = db.query(ProductionOrder).filter(ProductionOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production order not found")
    order.status = status
    if status == ProductionStatus.COMPLETE:
        from datetime import datetime
        order.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    return order
