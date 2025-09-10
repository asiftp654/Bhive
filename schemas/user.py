from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
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


class VerifyOtp(BaseModel):
    email: EmailStr
    otp: int


class UserVerifyResponse(BaseModel):
    message: str
    user: UserResponse
    access_token: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

