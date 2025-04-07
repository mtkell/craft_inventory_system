from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.db.database import Base

class ChangeType(PyEnum):
    RESTOCK = "restock"
    DEDUCTION = "deduction"

class InventoryChangeLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    production_order_id = Column(Integer, ForeignKey("production_orders.id"), nullable=True)
    change_type = Column(Enum(ChangeType), nullable=False)
    quantity = Column(Float, nullable=False)
    remaining = Column(Float, nullable=False)
    note = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    material = relationship("Material", back_populates="inventory_logs")
    production_order = relationship("ProductionOrder", backref="inventory_logs")
