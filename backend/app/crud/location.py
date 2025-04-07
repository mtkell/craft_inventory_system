from sqlalchemy.orm import Session
from app.models.location import Location
from app.schemas.location import LocationCreate

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Location).offset(skip).limit(limit).all()

def create_location(db: Session, location: LocationCreate):
    db_location = Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location
