#  Bhive - Mutual Fund Broker Application

A comprehensive FastAPI-based mutual fund investment platform that allows users to discover, invest in, and track their mutual fund portfolios

## 🚀 Features

### User Management
- **User Registration & Authentication**: Secure user signup with email verification
- **OTP Verification**: Email-based OTP system for account verification
- **JWT Authentication**: Token-based authentication for secure API access
- **User Login**: Secure login with password verification

### Investment Management
- **Mutual Fund Discovery**: Browse mutual funds by fund family
- **Investment Portfolio**: Create mutual fund investments
- **Automated Performance Tracking**: Track investment performance with hourly price updates via scheduled background tasks
- **Profit/Loss Calculation**: Automatic calculation of gains and losses
- **Portfolio Summary**: Complete overview of all investments with total P&L

### Background Processing
- **Automated Price Updates**: Celery-powered background tasks for real-time price synchronization
- **Email Notifications**: Asynchronous email sending for OTP verification
- **Redis Caching**: Fast data access and OTP storage with automatic expiration for enhanced performance


## 🏗️ Architecture

### Tech Stack
- **Backend**: FastAPI (Python 3.10)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache/Message Broker**: Redis for fast data access, OTP storage, and Celery task queue
- **Background Tasks**: Celery with Celery Beat
- **Authentication**: JWT tokens with bcrypt password hashing
- **Email**: SMTP integration for notifications
- **Containerization**: Docker & Docker Compose
- **Database Migrations**: Alembic


### Project Structure
```
Bhive/
├── api/                    # API route handlers
│   ├── user.py            # User authentication endpoints
│   ├── investments.py     # Investment management endpoints
│   └── utils.py           # Utility functions
├── models/                # SQLAlchemy database models
│   ├── user.py           # User model
│   └── investments.py    # Investment model
├── schemas/              # Pydantic schemas for API
│   ├── user.py          # User request/response schemas
│   └── investments.py   # Investment schemas
├── tests/               # Test files
│   ├── __init__.py      # Test package initialization
│   ├── conftest.py      # Test configuration and fixtures
│   ├── test_auth.py     # Authentication endpoint tests
│   └── test_investments.py # Investment endpoint tests
├── crud/                # Database operations
│   ├── user.py         # User CRUD operations
│   └── investments.py  # Investment CRUD operations
├── alembic/            # Database migration files
├── frontend/           # Frontend application
│   ├── index.html     # Main HTML page
│   ├── styles.css     # CSS styling
│   ├── main.js        # Application entry point
│   ├── auth.js        # Authentication handling
│   ├── investments.js # Investment management UI
│   ├── api.js         # API communication layer
│   └── server.py      # Static file server
├── main.py             # FastAPI application entry point
├── config.py           # Configuration settings
├── database.py         # Database connection setup
├── auth.py             # Authentication utilities
├── celery_app.py       # Celery configuration
├── tasks.py            # Background task definitions
└── docker-compose.yml  # Multi-container setup
```


## 🛠️ Installation & Setup

### Prerequisites
- Docker & Docker Compose

### Docker & Docker Compose Setup

#### Installation Guide

**For Windows & macOS:**
- Download and install [Docker Desktop](https://docs.docker.com/get-started/get-docker/)
- Docker Compose is included with Docker Desktop
- Once installed restart the system a
- After installation In powershee(In case of Windows) or In Terminal(In case of macOs), verify with:
  ```bash
  docker --version
  docker compose version
  ```

**For Linux (Ubuntu/Debian):**
```bash
# Quick installation script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Add user to docker group (optional, to avoid using sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

**For other Linux distributions:**
- Follow the [official Docker installation guide](https://docs.docker.com/engine/install/) for your specific distribution
- Install Docker Compose using the [official instructions](https://docs.docker.com/compose/install/)

#### Post-Installation Setup
```bash
# Test Docker installation
docker run hello-world
```

#### Troubleshooting
- **Permission denied errors**: Make sure your user is in the docker group or use `sudo`
- **Docker daemon not running**: Start Docker service with `sudo systemctl start docker` (Linux)
- **Port conflicts**: Ensure ports 8000, 5434, 6380, and 3000 are available

### Environment Variables
Create a `.env` file in the project root
Paste the env variables that were sent in the email.


### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Bhive
   ```

2. **Start all services**
   ```bash
   sudo docker-compose build
   sudo docker-compose up -d
   ```

3. **Verify the setup**
   ```bash
   # Check if all containers are running
   sudo docker-compose ps
   
   # View application logs
   sudo docker-compose logs web
   ```

The backend application will be available at: `http://localhost:8000`


## 🎨 Frontend

The frontend is a simple one, just created to showcase backend apis. 

It is served at `http://localhost:3000` 

when running with Docker Compose


## 🔌 RapidAPI Integration

The application integrates with [Latest Mutual Fund NAV API](https://rapidapi.com/suneetk92/api/latest-mutual-fund-nav).

A test account has been set up for you.

If you prefer to use your own key:

1. Log in to [RapidAPI](https://rapidapi.com/).
2. Search for latest-mutual-fund-nav by suneet92
3. Select the latest version of the API in the sidebar.
4. Subscribe to the API for free plan
5. Copy the X-RapidAPI-Key.
6. Paste it into the `.env` file as the value for:
   ```
   MUTUAL_FUND_API_KEY=your_rapidapi_key_here
   ```

## 📧 Email Integration

A sample email account has been created for sending OTPs during authentication.

Update the SMTP settings in the `.env` file if you want to use your own email provider.


## 📚 API Documentation

### Interactive API Documentation
- **Swagger UI**: `http://localhost:8000/docs`

### Postman API Collection
Access the comprehensive Postman collection that covers success & failure responses:
- **Collection Link**: [Bhive API Collection](https://www.postman.com/interstellar-station-763625/workspace/collab/collection/24617918-ed2d8e70-32a3-4420-a51c-e4ffe8b16f2c?action=share&source=copy-link&creator=24617918)


## 🧪 Testing

The project includes comprehensive test coverage for authentication and investment functionality using pytest and FastAPI's testing framework.

### Running Tests

#### Run All Tests
```bash
# From the project root directory
docker-compose run --rm tests
```

### Key Endpoints

#### Authentication
```
POST /users/signup          # User registration
POST /users/verify-otp      # Email verification
POST /users/login           # User login
```

#### Mutual Funds
```
GET  /mutual-funds                    # Get mutual funds by family
GET  /mutual-funds/investments        # Get user's investments
POST /mutual-funds/investments        # Create new investment
```


## 🔄 Background Tasks

### Automated Price Updates
The application includes a Celery-powered background task system that:
- **Fetches Latest Prices**: Retrieves current NAV values from the mutual fund API
- **Updates Database**: Bulk updates investment prices efficiently
- **Runs Hourly**: Scheduled to run every hour (3600 seconds) - configurable
- **Error Handling**: Automatic retries with exponential backoff


## 🔧 Configuration

### Key Configuration Options

- **JWT Settings**: Token expiration, secret key, algorithm
- **Database**: Connection pooling, timeout settings
- **Redis**: Connection settings for caching and task queue
- **Email**: SMTP server configuration for notifications
- **API Integration**: RapidAPI configuration for mutual fund data
- **Celery**: Task scheduling and worker configuration

