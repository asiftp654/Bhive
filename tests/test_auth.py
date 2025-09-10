import pytest


@pytest.mark.asyncio
async def test_signup_success(client):
    """Test successful user registration"""
    response = await client.post("/users/signup", json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["message"].startswith("User created successfully")
    assert data["user"]["email"] == "testuser@example.com"

@pytest.mark.asyncio
async def test_signup_duplicate_email(client):
    """Test signup with already registered email"""
    await client.post("/users/signup", json={
        "email": "duplicate@example.com",
        "password": "testpassword"
    })
    
    # Try to signup again with same email
    response = await client.post("/users/signup", json={
        "email": "duplicate@example.com",
        "password": "anotherpassword"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == 400
    assert data["message"] == "Email already registered"

@pytest.mark.asyncio
async def test_signup_invalid_email(client):
    """Test signup with invalid email format"""
    response = await client.post("/users/signup", json={
        "email": "invalid-email",
        "password": "testpassword"
    })
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_signup_short_password(client):
    """Test signup with password too short"""
    response = await client.post("/users/signup", json={
        "email": "shortpass@example.com",
        "password": "123"  # Less than 8 characters
    })
    assert response.status_code == 422 

@pytest.mark.asyncio
async def test_verify_otp_user_not_found(client):
    """Test OTP verification for non-existent user"""
    response = await client.post("/users/verify-otp", json={
        "email": "nonexistent@example.com",
        "otp": "123456"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == 400
    assert data["message"] == "User not found"

@pytest.mark.asyncio
async def test_verify_otp_invalid_otp(client):
    """Test OTP verification with invalid OTP"""
    await client.post("/users/signup", json={
        "email": "otptest@example.com",
        "password": "testpassword"
    })
    
    # Try to verify with invalid OTP
    response = await client.post("/users/verify-otp", json={
        "email": "otptest@example.com",
        "otp": "123456"  # invalid otp
    })
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == 400
    assert data["message"] == "Invalid OTP"

@pytest.mark.asyncio
async def test_login_unverified_user(client):
    """Test login with unverified user"""
    # Create user first
    await client.post("/users/signup", json={
        "email": "unverified@example.com",
        "password": "testpassword"
    })
    
    # Try to login without verification
    response = await client.post("/users/login", json={
        "email": "unverified@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == 400
    assert data["message"] == "Please verify your email first"

@pytest.mark.asyncio
async def test_login_user_not_found(client):
    """Test login with non-existent user"""
    response = await client.post("/users/login", json={
        "email": "nonexistent@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == 400
    assert data["message"] == "Invalid email or password"

@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """Test login with wrong password"""
    # Create user first
    await client.post("/users/signup", json={
        "email": "wrongpass@example.com",
        "password": "correctpassword"
    })
    
    # Try to login with wrong password
    response = await client.post("/users/login", json={
        "email": "wrongpass@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == 400
    assert data["message"] == "Invalid email or password"

@pytest.mark.asyncio
async def test_login_invalid_email_format(client):
    """Test login with invalid email format"""
    response = await client.post("/users/login", json={
        "email": "invalid-email-format",
        "password": "testpassword"
    })
    assert response.status_code == 422
