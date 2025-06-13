from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # База данных
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://telegram_sender:StrongPassword123!@localhost/telegram_sender_db"
    )
    
    # Redis
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    REDIS_URL: str = Field(default="redis://localhost:6379")
    
    # JWT
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # Приложение
    APP_NAME: str = Field(default="BotCast")
    DEBUG: bool = Field(default=False)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
