from pydantic import ConfigDict, BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class ClienteBase(BaseModel):
    """Schema base para Cliente"""
    razon_social: str
    nit: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_telefono: Optional[str] = None
    contacto_email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    estado: str = "ACTIVO"


class ClienteCreate(ClienteBase):
    """Schema para crear Cliente"""
    
    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: str) -> str:
        if v not in ["ACTIVO", "INACTIVO"]:
            raise ValueError("Estado debe ser ACTIVO o INACTIVO")
        return v


class ClienteUpdate(BaseModel):
    """Schema para actualizar Cliente"""
    razon_social: Optional[str] = None
    nit: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_telefono: Optional[str] = None
    contacto_email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    estado: Optional[str] = None
    
    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in ["ACTIVO", "INACTIVO"]:
            raise ValueError("Estado debe ser ACTIVO o INACTIVO")
        return v


class ClienteResponse(ClienteBase):
    """Schema para respuesta de Cliente"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Propiedades calculadas
    contacto_principal: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class ClienteReporte(BaseModel):
    """Schema para reporte de cliente"""
    id: int
    razon_social: str
    total_viajes: int
    volumen_carga_ton: float
    facturacion_total: float
    tipos_carga_frecuentes: list
    
    model_config = ConfigDict(from_attributes=True)