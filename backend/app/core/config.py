from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, model_validator
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Información de la aplicación
    APP_NAME: str = "Sistema de Gestión de Autotransporte"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Base de datos
    DATABASE_URL: Optional[str] = None
    DB_SERVER: str = "localhost"
    DB_NAME: str = "gestion_transporte"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    
    @model_validator(mode="after")
    def assemble_db_connection(self) -> 'Settings':
        if self.DATABASE_URL is None:
            # Para desarrollo local, usar SQLite con SQLAlchemy
            if self.ENVIRONMENT == "development":
                self.DATABASE_URL = "sqlite:///./gestion_transporte.db"
            else:
                self.DATABASE_URL = f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}/{self.DB_NAME}"
        return self
    
    # JWT
    SECRET_KEY: str = "tu_clave_secreta_super_segura_aqui_cambiala_en_produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:4200", "http://localhost:3000"]
    
    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # Configuración regional
    TIMEZONE: str = "America/La_Paz"
    LOCALE: str = "es_BO"
    CURRENCY: str = "BOB"
    
    # Logs
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Archivos
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()