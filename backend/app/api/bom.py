from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.schemas.bom import BoMCreate, BoMRead
from app.crud import bom as crud_bom
from app.models import bom as model_bom
from app.db.database import SessionLocal, engine
from app.utils.bom import calculate_materials_for_batch

model_bom.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/bom", tags=["Bill of Materials"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BoMRead, tags=["Bill of Materials"])
def create_bom_entry(
    bom: BoMCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new Bill of Materials (BoM) entry.

    - Users must provide a **product_id**, list of **materials**, and other relevant details.
    - The created BoM entry will be associated with the specified product.

    **Example Request**:
    ```json
    {
        "product_id": 1,
        "materials": [
            {"material_id": 1, "quantity": 10},
            {"material_id": 2, "quantity": 5}
        ]
    }
    ```

    **Example Response**:
    ```json
    {
        "id": 1,
        "product_id": 1,
        "materials": [
            {"material_id": 1, "quantity": 10},
            {"material_id": 2, "quantity": 5}
        ]
    }
    ```
    """
    return crud_bom.create_bom(db, bom)

@router.get("/", response_model=list[BoMRead], tags=["Bill of Materials"])
def list_bom_entries(
    product_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of BoM entries.

    - **product_id** is optional, if provided, will filter BoM entries by product.
    - Returns a list of BoM entries associated with products.

    **Example Request**:
    ```json
    {
        "product_id": 1
    }
    ```

    **Example Response**:
    ```json
    [
        {
            "id": 1,
            "product_id": 1,
            "materials": [
                {"material_id": 1, "quantity": 10},
                {"material_id": 2, "quantity": 5}
            ]
        },
        {
            "id": 2,
            "product_id": 1,
            "materials": [
                {"material_id": 3, "quantity": 8}
            ]
        }
    ]
    ```
    """
    return crud_bom.get_boms(db, product_id=product_id)

@router.get("/calculate/", tags=["Bill of Materials"])
def calculate_materials(
    product_id: int,
    batch_size: int = 1,
    check_availability: bool = False,
    db: Session = Depends(get_db)
):
    """
    Calculate the materials required for a specific batch size.

    - **product_id** specifies the product for which the materials need to be calculated.
    - **batch_size** determines the number of units to calculate materials for.
    - **check_availability** (optional) checks material availability in inventory.
    
    **Example Request**:
    ```json
    {
        "product_id": 1,
        "batch_size": 10,
        "check_availability": true
    }
    ```

    **Example Response**:
    ```json
    {
        "materials_required": [
            {"material_id": 1, "quantity_needed": 100, "available_in_inventory": 50},
            {"material_id": 2, "quantity_needed": 50, "available_in_inventory": 40}
        ],
        "status": "insufficient materials"
    }
    ```
    """
    return calculate_materials_for_batch(db, product_id, batch_size, check_availability)
