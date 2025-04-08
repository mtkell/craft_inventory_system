from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.schemas.auth import UserCreate, UserRead, Token
from app.services.auth_utils import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserRead, tags=["Authentication"])
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    - Users must provide a **username**, **email**, **full_name**, and **password**.
    - **Username** should be unique.

    **Example Request**:
    ```
    {
      "username": "newuser",
      "email": "newuser@example.com",
      "full_name": "New User",
      "password": "securepassword"
    }
    ```
    **Example Response**:
    ```
    {
      "id": 1,
      "username": "newuser",
      "email": "newuser@example.com",
      "full_name": "New User"
    }
    ```
    """
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token, tags=["Authentication"])
def login(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    User login endpoint to authenticate and obtain a JWT token.

    - Users need to provide **username** and **password** to authenticate.
    - On success, an **access_token** is returned.

    **Example Request**:
    ```
    {
      "username": "existinguser",
      "password": "correctpassword"
    }
    ```
    **Example Response**:
    ```
    {
      "access_token": "jwt_token_string",
      "token_type": "bearer"
    }
    ```
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
