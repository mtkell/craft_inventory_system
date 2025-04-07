from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.production_audit_log import ProductionAuditLog
from app.schemas.production_audit_log import ProductionAuditLogRead
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from typing import List

router = APIRouter(prefix="/production_orders", tags=["Production Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{order_id}/audit", response_model=List[ProductionAuditLogRead])
def get_audit_logs(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "operator"))
):
    logs = db.query(ProductionAuditLog).filter(
        ProductionAuditLog.production_order_id == order_id
    ).order_by(ProductionAuditLog.timestamp.desc()).all()

    if not logs:
        raise HTTPException(status_code=404, detail="No audit logs found for this production order")

    return logs
