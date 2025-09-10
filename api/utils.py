import requests
import jwt
import random
import asyncio
import aiosmtplib
import requests
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database import redis_client
from passlib.context import CryptContext
from config import settings


def hash_password(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)  


def generate_otp(user_email: str) -> str:
    otp = str(random.randint(100000, 999999))
    key = f"otp:{user_email}"
    redis_client.setex(key, 300, otp)
    return otp

def verify_otp(user_email: str, otp: int) -> bool:
    key = f"otp:{user_email}"
    stored_otp = redis_client.get(key)
    print(stored_otp)

    if stored_otp and stored_otp.decode() == str(otp):
        redis_client.delete(key)
        return True
    return False

async def send_otp(email: str, otp: str) -> bool:
    subject = f"Your OTP Code [{otp}] - MF Brokers"
    text_content = f"""
    Hello,

    Your One-Time Password (OTP) is: {otp}

    This OTP is valid for 5 minutes.

    Do not share this code with anyone.

    - MF Brokers Team
    """
    
    try:
        return await send_email(email, subject, text_content)
    except Exception as e:
        print(f"Error sending OTP to {email}: {str(e)}")
        return False

async def send_email(recipient_email: str, subject: str, text_content: str = None) -> bool:
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"MF Brokers <{settings.sender_email}>"
        message["To"] = recipient_email

        
        text_part = MIMEText(text_content, "plain")
        message.attach(text_part)

        await aiosmtplib.send(
            message,
            hostname=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password,
            start_tls=True,
        )        
        return True
    
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {str(e)}")
        return False

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.PyJWTError:
        return None

def get_current_user(db, token: str):
    """
    Get current user from JWT token
    """
    try:
        payload = verify_token(token)
        if payload is None:
            return None
        
        user_email = payload.get("sub")
        user_id = payload.get("user_id")
        
        if user_email is None or user_id is None:
            return None
            
        # Import here to avoid circular imports
        from models.user import User
        user = db.query(User).filter(User.id == user_id, User.email == user_email).first()
        return user
        
    except Exception:
        return None


def call_rapidapi(querystring: dict) -> dict:
    try:
        url = settings.mutual_fund_api_url
        headers = {
            "x-rapidapi-key": settings.mutual_fund_api_key,
            "x-rapidapi-host": settings.mutual_fund_api_host
        }
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 429:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Monthly API quota exceeded. Please use different API key."
            )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error calling RapidAPI: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while fetching data"
        )