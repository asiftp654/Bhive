import pytest


@pytest.mark.asyncio
async def test_get_mutual_funds_unauthorized(client):
    """Test getting mutual funds without authentication"""
    response = await client.get("/mutual-funds?fund_family=TestFamily")
    assert response.status_code == 403 

@pytest.mark.asyncio
async def test_get_mutual_funds_missing_parameter(client):
    """Test getting mutual funds without required fund_family parameter"""
    response = await client.get("/mutual-funds")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_investment_unauthorized(client):
    """Test creating investment without authentication"""
    response = await client.post("/mutual-funds/investments", json={
        "scheme_code": "123456",
        "units": 10.0
    })
    assert response.status_code == 403 

@pytest.mark.asyncio
async def test_create_investment_missing_fields(client):
    """Test creating investment with missing required fields"""
    response = await client.post("/mutual-funds/investments", json={})
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_endpoints_with_invalid_json(client):
    """Test endpoints with malformed JSON"""
    response = await client.post("/mutual-funds/investments",
                               data="invalid json",
                               headers={"Content-Type": "application/json"})
    assert response.status_code == 422
