from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from api.utils import get_current_user
from models.user import User

# Security scheme for Bearer token
security = HTTPBearer()

def get_current_active_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user
    This will be used to protect routes that require authentication
    """
    token = credentials.credentials
    
    user = get_current_user(db, token)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User | None:
    """
    Optional dependency to get current user
    Returns None if no valid token is provided
    Useful for endpoints that work with or without authentication
    """
    try:
        token = credentials.credentials
        user = get_current_user(db, token)
        
        if user and user.is_verified:
            return user
        return None
    except:
        return None