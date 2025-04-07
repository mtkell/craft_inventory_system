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

@router.post("/", response_model=LocationRead)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    return crud_location.create_location(db=db, location=location)

@router.get("/", response_model=list[LocationRead])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_location.get_locations(db, skip=skip, limit=limit)
