from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class ProductionAuditLog(Base):
    __tablename__ = "production_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    production_order_id = Column(Integer, ForeignKey("production_orders.id"), nullable=False)
    action = Column(String, nullable=False)  # e.g., "created", "completed", "cancelled"
    note = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    production_order = relationship("ProductionOrder", backref="audit_logs")
