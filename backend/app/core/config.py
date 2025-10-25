from typing import Optional
from pydantic import (
    ConfigDict,
    PostgresDsn,
    computed_field
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
import secrets

class Settings(BaseSettings):
    
    # Security Settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Server Configuration
    DOMAIN: str = "localhost"  # You should define this in the environment if needed
    ENVIRONMENT: str = "local"  # Same for this one if you want to configure it from the environment
    DEBUG: bool = False  # Pydantic will automatically read this from the environment
    
    
    #CORS
    CORS_ALLOW_ORIGINS: list[str] = []

    # ----------------------------------
    # Server Host Computed Field
    # ----------------------------------
    @computed_field
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
    
    
    
    POSTGRES_SERVER: str
    POSTGRES_PORT: Optional[int] = None
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""
    LOGFIRE_TOKEN: str = ""
    LOGFIRE_LOCAL: bool = False
    
    
    
    
     # Database Configuration
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

# Initialize settings
settings = Settings()