from pydantic import BaseModel, EmailStr, field_validator
from typing import Union, List


class BaseEmailModel(BaseModel):
    email: EmailStr
    
    @field_validator('email')
    @classmethod
    def normalize_email(cls, v):
        return v.lower()


class UserCreate(BaseEmailModel):
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserResponse(BaseModel):
    email: str
    name: str
    
    class Config:
        from_attributes = True


class UserCreateResponse(BaseModel):
    message: str
    user: UserResponse


class VerifyOtp(BaseEmailModel):
    otp: int


class UserVerifyResponse(BaseModel):
    user: UserResponse
    access_token: str


class UserLogin(BaseEmailModel):
    password: str


class ErrorResponse(BaseModel):
    code: int
    message: Union[str, List[str]]