from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    location_id = Column(Integer, ForeignKey("locations.id"))

    location = relationship("Location")
