from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.location import LocationCreate, LocationRead
from app.crud import location as crud_location
from app.models import location as model_location
from app.db.database import SessionLocal, engine

model_location.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/locations", tags=["Locations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=LocationRead, tags=["Locations"])
def create_location(
    location: LocationCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new location.

    - **location**: The request body should contain the name, address, and any other relevant location details.
    
    **Example Request**:
    ```json
    {
        "name": "Warehouse 1",
        "address": "123 Warehouse St."
    }
    ```

    **Example Response**:
    ```json
    {
        "id": 1,
        "name": "Warehouse 1",
        "address": "123 Warehouse St."
    }
    ```
    """
    return crud_location.create_location(db=db, location=location)

@router.get("/", response_model=list[LocationRead], tags=["Locations"])
def read_locations(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all locations.

    - **skip**: Number of records to skip (used for pagination).
    - **limit**: The maximum number of records to return. Default is 100.

    **Example Request**:
    ```json
    {
        "skip": 0,
        "limit": 10
    }
    ```

    **Example Response**:
    ```json
    [
        {
            "id": 1,
            "name": "Warehouse 1",
            "address": "123 Warehouse St."
        },
        {
            "id": 2,
            "name": "Warehouse 2",
            "address": "456 Warehouse Ave."
        }
    ]
    ```

    """
    return crud_location.get_locations(db, skip=skip, limit=limit)
