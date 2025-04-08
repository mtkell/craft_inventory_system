from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.material import Material

router = APIRouter(prefix="/materials", tags=["Materials"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/low_stock/", tags=["Materials"])
def get_low_stock_materials(db: Session = Depends(get_db)):
    """
    Retrieve materials that are below their reorder point (low stock).

    - Returns materials with a quantity lower than the defined reorder point.
    
    **Example Request**:
    No request body required for this endpoint.

    **Example Response**:
    ```json
    [
        {
            "id": 1,
            "name": "Material A",
            "quantity": 5,
            "unit": "kg",
            "reorder_point": 10
        },
        {
            "id": 2,
            "name": "Material B",
            "quantity": 3,
            "unit": "m",
            "reorder_point": 7
        }
    ]
    ```
    """
    materials = db.query(Material).filter(Material.quantity < Material.reorder_point).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "quantity": m.quantity,
            "unit": m.unit,
            "reorder_point": m.reorder_point
        }
        for m in materials
    ]
