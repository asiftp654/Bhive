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
├── crud/                # Database operations
│   ├── user.py         # User CRUD operations
│   └── investments.py  # Investment CRUD operations
├── alembic/            # Database migration files
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
- Python 3.10+
- Docker & Docker Compose

### Environment Variables
Create a `.env` file in the project root
Paste the env variables that were sent in the email.

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Bhive
   ```

2. **Create environment file**
   ```bash
   nano .env
   # Paste all env variables that were sent in the email.
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Verify the setup**
   ```bash
   # Check if all containers are running
   docker-compose ps
   
   # View application logs
   docker-compose logs web
   ```

The application will be available at: `http://localhost:8000`


## 🔌 RapidAPI Integration

The application integrates with [Latest Mutual Fund NAV API](https://rapidapi.com/suneetk92/api/latest-mutual-fund-nav).

A test account has been set up for you.

If you prefer to use your own key:

1. Log in to [RapidAPI](https://rapidapi.com/).
2. Search for latest-mutual-fund-nav by suneet92
2. Select the latest version of the API in the sidebar.
3. Copy the X-RapidAPI-Key.
4. Paste it into the `.env` file as the value for:
   ```
   MUTUAL_FUND_API_KEY=your_rapidapi_key_here
   ```

## 📧 Email Integration

A sample email account has been created for sending OTPs during authentication.

Update the SMTP settings in the `.env` file if you want to use your own email provider.


## 📚 API Documentation

### Interactive API Documentation
- **Swagger UI**: `http://localhost:8000/docs`

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


**Built with ❤️ using FastAPI, PostgreSQL, Redis, and Celery**
