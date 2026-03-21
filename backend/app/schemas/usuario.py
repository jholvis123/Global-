from pydantic import ConfigDict, BaseModel, EmailStr, field_validator
from typing import List, Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    """Schema base para Usuario"""
    email: EmailStr
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    estado: Optional[str] = "ACTIVO"


class UsuarioCreate(UsuarioBase):
    """Schema para crear Usuario"""
    password: str
    roles: List[str] = []
    
    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v
    
    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: Optional[str]) -> Optional[str]:
        if v not in ["ACTIVO", "INACTIVO", "BLOQUEADO"]:
            raise ValueError("Estado debe ser ACTIVO, INACTIVO o BLOQUEADO")
        return v


class UsuarioUpdate(BaseModel):
    """Schema para actualizar Usuario"""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    estado: Optional[str] = None
    password: Optional[str] = None
    roles: Optional[List[str]] = None
    
    @field_validator("password")
    @classmethod
    def validar_password(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v


class UsuarioResponse(UsuarioBase):
    """Schema para respuesta de Usuario"""
    id: int
    roles: List[str] = []
    intentos_fallidos: int
    ultimo_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    """Schema para request de login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema para respuesta de tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    usuario: UsuarioResponse


class ChangePasswordRequest(BaseModel):
    """Schema para cambio de contraseña"""
    password_actual: str
    password_nueva: str
    
    @field_validator("password_nueva")
    @classmethod
    def validar_password_nueva(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La nueva contraseña debe tener al menos 8 caracteres")
        return v