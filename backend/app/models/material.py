from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.inventory_log import InventoryChangeLog  # New import

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Float, default=0.0)  # In yards, meters, or units
    unit = Column(String, default="yards")  # e.g., yards, meters, pieces
    reorder_point = Column(Float, default=0.0)  # minimum required quantity

    # 🔁 Inventory change logs
    inventory_logs = relationship(
        "InventoryChangeLog",
        back_populates="material",
        cascade="all, delete"
    )
