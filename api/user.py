from fastapi import APIRouter, status, HTTPException, Depends, BackgroundTasks
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import get_db
from crud.user import UserCrud
from schemas.user import UserCreate, UserCreateResponse, VerifyOtp, UserVerifyResponse, UserLogin
from api.utils import (verify_password, generate_otp, verify_otp, send_otp,
                       create_access_token)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
async def signup(data: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user_crud = UserCrud(db)    
    existing_user = user_crud.get_user(data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Try Except to handle IntegrityError (Incase of concurrent requests)   
    try:
        user = user_crud.create_user(data.email, data.password)
        
        # Generate OTP and send it in the background
        otp = generate_otp(data.email)
        background_tasks.add_task(send_otp, data.email, otp)

        return {
            "message": "User created successfully. Please check your email for OTP.",
            "user": user
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

@router.post("/verify-otp", status_code=status.HTTP_200_OK, response_model=UserVerifyResponse)
def validate_otp(data: VerifyOtp, db: Session = Depends(get_db)):
    user_crud = UserCrud(db)
    user = user_crud.get_user(data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    if not verify_otp(data.email, data.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    user = user_crud.mark_as_verified(user)
    
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {
        "message": "OTP verified successfully", 
        "user": user,
        "access_token": access_token
    }


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserVerifyResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = UserCrud(db).get_user(data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please verify your email first"
        )
    
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})    
    return UserVerifyResponse(
        message="Login successful",
        user=user,
        access_token=access_token
    )