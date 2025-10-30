import os
import json
from typing import Optional, Any
from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Settings(BaseSettings):
    
    # Información básica
    PROJECT_NAME: str = "Zucane Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Base de datos
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_USER: str = "user"
    DB_PASSWORD: str = "pass"
    DB_NAME: str = "zucane_db"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+mysqldb://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Stellar Network (SOLO desde variables de entorno)
    STELLAR_HORIZON_URL: str = "https://horizon-testnet.stellar.org"
    STELLAR_NETWORK: str = "testnet"
    GOVERNMENT_PUBLIC_KEY: str = ""
    GOVERNMENT_SECRET_KEY: str = ""
    TREASURY_PUBLIC_KEY: str = ""
    TREASURY_SECRET_KEY: str = ""
    ASSET_NAME: str = "XOCHI"
    HORIZON_URL: str = "https://horizon-testnet.stellar.org"

    # Alias para compatibilidad con nombres solicitados
    @property
    def ISSUER_P(self) -> str:
        return self.GOVERNMENT_PUBLIC_KEY

    @property
    def ISSUER_S(self) -> str:
        return self.GOVERNMENT_SECRET_KEY

    @property
    def TREASURY_P(self) -> str:
        return self.TREASURY_PUBLIC_KEY

    @property
    def TREASURY_S(self) -> str:
        return self.TREASURY_SECRET_KEY

    # Mapa de negocios: public -> secret (desde ENV opcional: BUSINESS_DB como JSON)
    BUSINESS_DB: dict = {}
    
    @field_validator("BUSINESS_DB", mode="before")
    @classmethod
    def parse_business_db(cls, v: Any) -> Any:
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return {}
        return v
    
    # Configuración de seguridad
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Campos adicionales del .env
    ALGORITHM: str = "HS256"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )


# Instancia global de configuración
settings = Settings()
