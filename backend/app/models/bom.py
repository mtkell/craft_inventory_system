from sqlalchemy import Column, Integer, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base

class BillOfMaterial(Base):
    __tablename__ = "bill_of_materials"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    quantity = Column(Float, nullable=False)

    product = relationship("Product")
    material = relationship("Material")

    __table_args__ = (
        UniqueConstraint("product_id", "material_id", name="uix_product_material"),
    )
