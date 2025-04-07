from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.dependencies.auth import get_current_user

def require_roles(*roles: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{current_user.role}' is not permitted to access this resource."
            )
        return current_user
    return role_checker
