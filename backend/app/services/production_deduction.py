from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.production_order import ProductionOrder
from app.models.bom import BillOfMaterial
from app.models.material import Material
from app.models.inventory_log import InventoryChangeLog, ChangeType
from app.models.production_audit_log import ProductionAuditLog

def deduct_for_production_order(order: ProductionOrder, db: Session):
    bom_items = db.query(BillOfMaterial).filter(BillOfMaterial.product_id == order.product_id).all()
    if not bom_items:
        raise HTTPException(status_code=400, detail="No BoM defined for this product")

    for item in bom_items:
        required_qty = item.quantity * order.batch_size
        material = db.query(Material).filter(Material.id == item.material_id).first()

        if not material:
            raise HTTPException(status_code=404, detail=f"Material ID {item.material_id} not found")
        if material.quantity < required_qty:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {material.name}: requires {required_qty}, has {material.quantity}"
            )

        material.quantity -= required_qty

        db.add(InventoryChangeLog(
            material_id=material.id,
            production_order_id=order.id,
            change_type=ChangeType.DEDUCTION,
            quantity=required_qty,
            remaining=material.quantity,
            note=f"Deduction for production order #{order.id}"
        ))

    # Automatically update order status
    if order.status == "planned":
        order.status = "in_progress"
    order.status = "complete"
    order.completed_at = datetime.utcnow()

    db.add(ProductionAuditLog(
        production_order_id=order.id,
        action="completed",
        note="Auto-complete after deduction"
    ))

    db.commit()
