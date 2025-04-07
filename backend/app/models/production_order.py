from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.db.database import Base

class ProductionStatus(PyEnum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"

class ProductionOrder(Base):
    __tablename__ = "production_orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    batch_size = Column(Integer, nullable=False)
    status = Column(Enum(ProductionStatus), default=ProductionStatus.PLANNED)
    note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    product = relationship("Product", back_populates="production_orders")
