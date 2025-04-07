from sqlalchemy.orm import Session
from app.models.bom import BillOfMaterial

def calculate_materials_for_batch(db: Session, product_id: int, batch_size: int = 1, check_availability: bool = False) -> dict:
    boms = db.query(BillOfMaterial).filter(BillOfMaterial.product_id == product_id).all()
    results = {}
    insufficient = {}

    for bom in boms:
        material_name = bom.material.name if bom.material else f"Material #{bom.material_id}"
        required_qty = round(bom.quantity * batch_size, 2)
        available_qty = bom.material.quantity if bom.material else 0

        results[material_name] = {
            "required": required_qty,
            "available": available_qty,
            "unit": bom.material.unit if bom.material else "",
            "status": "ok"
        }

        if check_availability and available_qty < required_qty:
            results[material_name]["status"] = "insufficient"
            insufficient[material_name] = {
                "required": required_qty,
                "available": available_qty
            }

    return {
        "product_id": product_id,
        "batch_size": batch_size,
        "materials": results,
        "insufficient": insufficient if check_availability else None
    }
