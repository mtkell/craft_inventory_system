from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.material import Material
from app.models.inventory_log import InventoryChangeLog, ChangeType
from app.schemas.material_restock import MaterialRestockRequest
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/materials", tags=["Materials"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/restock/", tags=["Materials"])
def restock_material(
    data: MaterialRestockRequest,
    db: Session = Depends(get_db)
):
    """
    Restock a material in the inventory.

    - **material_id**: The ID of the material to be restocked.
    - **quantity**: The amount of material to be added to inventory.
    - **note**: An optional note describing the restock.

    **Example Request**:
    ```json
    {
        "material_id": 1,
        "quantity": 50,
        "note": "Manual restock"
    }
    ```

    **Example Response**:
    ```json
    {
        "status": "success",
        "message": "Material 'Material A' restocked by 50. New total: 150"
    }
    ```

    **Error Response** (Material not found):
    ```json
    {
        "detail": "Material not found"
    }
    ```

    **Error Response** (Database error):
    ```json
    {
        "detail": "Failed to restock material due to database error."
    }
    ```
    """
    try:
        with db.begin():
            material = db.query(Material).filter(Material.id == data.material_id).first()
            if not material:
                raise HTTPException(status_code=404, detail="Material not found")

            material.quantity += data.quantity

            db.add(InventoryChangeLog(
                material_id=material.id,
                change_type=ChangeType.RESTOCK,
                quantity=data.quantity,
                remaining=material.quantity,
                note=data.note or "Manual restock"
            ))

            db.commit()
            return {
                "status": "success",
                "message": f"Material '{material.name}' restocked by {data.quantity}. New total: {material.quantity}"
            }

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to restock material due to database error.")
