from pydantic import ConfigDict, BaseModel, field_validator
from typing import Optional
from decimal import Decimal
from datetime import datetime


class AnticipoBase(BaseModel):
    """Schema base para Anticipo"""
    beneficiario_tipo: str
    monto_bs: Decimal
    fecha: datetime
    observacion: Optional[str] = None
    viaje_id: Optional[int] = None
    socio_id: Optional[int] = None
    chofer_id: Optional[int] = None


class AnticipoCreate(AnticipoBase):
    """Schema para crear Anticipo"""
    
    @field_validator("beneficiario_tipo")
    @classmethod
    def validar_beneficiario_tipo(cls, v: str) -> str:
        if v not in ["SOCIO", "CHOFER"]:
            raise ValueError("Beneficiario tipo debe ser SOCIO o CHOFER")
        return v
    
    @field_validator("monto_bs")
    @classmethod
    def validar_monto(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return v
    
    @field_validator("socio_id")
    @classmethod
    def validar_socio_id(cls, v: Optional[int], info) -> Optional[int]:
        if info.data.get("beneficiario_tipo") == "SOCIO" and not v:
            raise ValueError("Se requiere socio_id para beneficiario tipo SOCIO")
        return v
    
    @field_validator("chofer_id")
    @classmethod
    def validar_chofer_id(cls, v: Optional[int], info) -> Optional[int]:
        if info.data.get("beneficiario_tipo") == "CHOFER" and not v:
            raise ValueError("Se requiere chofer_id para beneficiario tipo CHOFER")
        return v


class AnticipoUpdate(BaseModel):
    """Schema para actualizar Anticipo"""
    observacion: Optional[str] = None
    estado: Optional[str] = None
    
    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in ["PENDIENTE", "LIQUIDADO"]:
            raise ValueError("Estado debe ser PENDIENTE o LIQUIDADO")
        return v


class AnticipoResponse(AnticipoBase):
    """Schema para respuesta de Anticipo"""
    id: int
    estado: str
    created_at: datetime
    updated_at: datetime
    
    # Datos del beneficiario
    beneficiario_nombre: str
    
    # Propiedades calculadas
    monto_formateado: str
    es_para_viaje_especifico: bool
    
    # Información del viaje (si aplica)
    viaje_origen: Optional[str] = None
    viaje_destino: Optional[str] = None
    viaje_fecha: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
        


class AnticipoReporte(BaseModel):
    """Schema para reporte de anticipos"""
    beneficiario_tipo: str
    beneficiario_id: int
    beneficiario_nombre: str
    total_anticipos: Decimal
    anticipos_pendientes: Decimal
    anticipos_liquidados: Decimal
    cantidad_anticipos: int
    
    model_config = ConfigDict(from_attributes=True)