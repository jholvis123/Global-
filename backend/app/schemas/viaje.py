from pydantic import ConfigDict, BaseModel, field_validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class ViajeBase(BaseModel):
    """Schema base para Viaje"""
    cliente_id: int
    vehiculo_id: int
    chofer_id: int
    origen: str
    destino: str
    fecha_salida: datetime
    fecha_llegada: Optional[datetime] = None
    tipo_carga: str
    peso_ton: Decimal
    volumen_m3: Optional[Decimal] = None
    km_estimado: int
    km_real: Optional[int] = None
    tarifa_tipo: str
    tarifa_valor: Decimal
    notas: Optional[str] = None


class ViajeCreate(ViajeBase):
    """Schema para crear Viaje"""
    
    @field_validator("tarifa_tipo")
    @classmethod
    def validar_tarifa_tipo(cls, v: str) -> str:
        if v not in ["KM", "TON", "FIJA"]:
            raise ValueError("Tipo de tarifa debe ser KM, TON o FIJA")
        return v
    
    @field_validator("peso_ton")
    @classmethod
    def validar_peso(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("El peso debe ser mayor a 0")
        return v
    
    @field_validator("km_estimado")
    @classmethod
    def validar_km_estimado(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Los kilómetros estimados deben ser mayor a 0")
        return v
    
    @field_validator("tarifa_valor")
    @classmethod
    def validar_tarifa_valor(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("El valor de la tarifa debe ser mayor a 0")
        return v


class ViajeUpdate(BaseModel):
    """Schema para actualizar Viaje"""
    fecha_llegada: Optional[datetime] = None
    km_real: Optional[int] = None
    estado: Optional[str] = None
    notas: Optional[str] = None
    
    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in ["PLANIFICADO", "EN_RUTA", "ENTREGADO", "LIQUIDADO"]:
            raise ValueError("Estado debe ser PLANIFICADO, EN_RUTA, ENTREGADO o LIQUIDADO")
        return v


class GastoViajeBase(BaseModel):
    """Schema base para GastoViaje"""
    tipo: str
    monto_bs: Decimal
    descripcion: Optional[str] = None
    soporte_url: Optional[str] = None
    fecha: datetime


class GastoViajeCreate(GastoViajeBase):
    """Schema para crear GastoViaje"""
    
    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        if v not in ["COMBUSTIBLE", "PEAJE", "VIATICO", "TALLER", "OTRO"]:
            raise ValueError("Tipo debe ser COMBUSTIBLE, PEAJE, VIATICO, TALLER u OTRO")
        return v
    
    @field_validator("monto_bs")
    @classmethod
    def validar_monto(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return v


class GastoViajeResponse(GastoViajeBase):
    """Schema para respuesta de GastoViaje"""
    id: int
    viaje_id: int
    created_at: datetime
    monto_formateado: str
    
    model_config = ConfigDict(from_attributes=True)


class ViajeResponse(ViajeBase):
    """Schema para respuesta de Viaje"""
    id: int
    estado: str
    created_at: datetime
    updated_at: datetime
    
    # Datos relacionados
    cliente_nombre: Optional[str] = None
    vehiculo_placa: Optional[str] = None
    chofer_nombre: Optional[str] = None
    socio_nombre: Optional[str] = None
    
    # Propiedades calculadas
    ingreso_total_bs: float
    total_gastos_bs: float
    margen_bruto_bs: float
    ruta_completa: str
    puede_cerrar: bool
    
    # Gastos del viaje
    gastos: List[GastoViajeResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class ViajeDetalle(ViajeResponse):
    """Schema detallado para respuesta de Viaje con toda la información"""
    # Información completa de entidades relacionadas
    cliente: Optional[dict] = None
    vehiculo: Optional[dict] = None
    chofer: Optional[dict] = None
    
    model_config = ConfigDict(from_attributes=True)


class CerrarViajeRequest(BaseModel):
    """Schema para cerrar un viaje"""
    fecha_llegada: datetime
    km_real: int
    notas: Optional[str] = None
    
    @field_validator("km_real")
    @classmethod
    def validar_km_real(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Los kilómetros reales deben ser mayor a 0")
        return v