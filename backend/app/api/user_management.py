from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User, UserCreate, UserRead
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles

router = APIRouter(prefix="/users", tags=["Users", "User Management"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserRead, tags=["Users", "User Management"])
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    Register a new user.

    - Only **admin** role can create new users.
    """
    db_user = User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=list[UserRead], tags=["Users", "User Management"])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    """
    List all registered users.

    - **admin** role can list users.
    """
    return db.query(User).all()
