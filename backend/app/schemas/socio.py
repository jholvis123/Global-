from pydantic import ConfigDict, BaseModel, field_validator
from typing import Optional
from decimal import Decimal
from datetime import datetime


class SocioBase(BaseModel):
    """Schema base para Socio"""
    nombre: str
    nit: Optional[str] = None
    ci: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    cuenta_bancaria: Optional[str] = None
    banco: Optional[str] = None
    participacion_tipo: str = "NETO"
    participacion_valor: Decimal
    estado: str = "ACTIVO"


class SocioCreate(SocioBase):
    """Schema para crear Socio"""
    
    @field_validator("participacion_tipo")
    @classmethod
    def validar_participacion_tipo(cls, v: str) -> str:
        if v not in ["NETO", "BRUTO"]:
            raise ValueError("Tipo de participación debe ser NETO o BRUTO")
        return v
    
    @field_validator("participacion_valor")
    @classmethod
    def validar_participacion_valor(cls, v: Decimal) -> Decimal:
        if v <= 0 or v > 100:
            raise ValueError("Participación debe estar entre 0 y 100")
        return v
    
    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: str) -> str:
        if v not in ["ACTIVO", "INACTIVO"]:
            raise ValueError("Estado debe ser ACTIVO o INACTIVO")
        return v


class SocioUpdate(BaseModel):
    """Schema para actualizar Socio"""
    nombre: Optional[str] = None
    nit: Optional[str] = None
    ci: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    cuenta_bancaria: Optional[str] = None
    banco: Optional[str] = None
    participacion_tipo: Optional[str] = None
    participacion_valor: Optional[Decimal] = None
    estado: Optional[str] = None
    
    @field_validator("participacion_tipo")
    @classmethod
    def validar_participacion_tipo(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in ["NETO", "BRUTO"]:
            raise ValueError("Tipo de participación debe ser NETO o BRUTO")
        return v
    
    @field_validator("participacion_valor")
    @classmethod
    def validar_participacion_valor(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v and (v <= 0 or v > 100):
            raise ValueError("Participación debe estar entre 0 y 100")
        return v


class SocioResponse(SocioBase):
    """Schema para respuesta de Socio"""
    id: int
    saldo_anticipos: Decimal
    created_at: datetime
    updated_at: datetime
    
    # Propiedades calculadas
    es_persona_natural: bool
    identificacion_principal: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# class SocioReporte(BaseModel):
#     """Schema para reporte de socio"""
#     id: int
#     nombre: str
#     total_viajes: int
#     ingresos_generados: Decimal
#     anticipos_recibidos: Decimal
#     saldo_final: Decimal
#     vehiculos_cantidad: int
    
#     model_config = ConfigDict(from_attributes=True)
