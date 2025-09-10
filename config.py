from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")
    redis_db: int = Field(..., env="REDIS_DB")
    
    # Email Configuration
    smtp_server: str = Field(..., env="SMTP_SERVER")
    smtp_port: int = Field(..., env="SMTP_PORT")
    smtp_username: str = Field(..., env="SMTP_USERNAME")
    smtp_password: str = Field(..., env="SMTP_PASSWORD")
    sender_email: str = Field(..., env="SENDER_EMAIL")
    
    debug: bool = Field(..., env="DEBUG")
    
    # JWT Configuration
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    mutual_fund_api_url: str = Field(..., env="MUTUAL_FUND_API_URL")
    mutual_fund_api_host: str = Field(..., env="MUTUAL_FUND_API_HOST")
    mutual_fund_api_key: str = Field(..., env="MUTUAL_FUND_API_KEY")
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
    
    @property
    def database_url(self) -> str:
        # Constructing the database URL
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()