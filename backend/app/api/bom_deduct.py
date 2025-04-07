from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.bom import BillOfMaterial
from app.models.material import Material
from app.models.inventory_log import InventoryChangeLog, ChangeType  # ✅ New import
from app.schemas.bom import BoMCreate, BoMRead
from app.utils.bom import calculate_materials_for_batch
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/bom", tags=["Bill of Materials"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/deduct/")
def deduct_inventory(product_id: int, batch_size: int, db: Session = Depends(get_db)):
    try:
        # Start transaction
        with db.begin():
            boms = db.query(BillOfMaterial).filter(BillOfMaterial.product_id == product_id).all()
            insufficient = []

            for bom in boms:
                material = db.query(Material).filter(Material.id == bom.material_id).first()
                if not material:
                    continue

                required_qty = round(bom.quantity * batch_size, 2)
                if material.quantity < required_qty:
                    insufficient.append({
                        "material": material.name,
                        "required": required_qty,
                        "available": material.quantity
                    })

            if insufficient:
                raise HTTPException(status_code=422, detail={"insufficient": insufficient})

            # Deduct from inventory and log the change
            for bom in boms:
                material = db.query(Material).filter(Material.id == bom.material_id).first()
                material.quantity -= round(bom.quantity * batch_size, 2)

                db.add(InventoryChangeLog(
                    material_id=material.id,
                    change_type=ChangeType.DEDUCTION,
                    quantity=round(bom.quantity * batch_size, 2),
                    remaining=material.quantity,
                    note=f"Auto deduction for batch of size {batch_size}"
                ))

            db.commit()
            return {
                "status": "success",
                "message": f"Inventory deducted for {batch_size} unit(s) of product {product_id}"
            }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to deduct inventory due to database error.")
