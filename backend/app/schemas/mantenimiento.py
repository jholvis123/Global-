from pydantic import ConfigDict, BaseModel, field_validator
from typing import Optional
from decimal import Decimal
from datetime import datetime, date


class MantenimientoBase(BaseModel):
    """Schema base para Mantenimiento"""
    vehiculo_id: int
    tipo: str
    descripcion: str
    costo_bs: Decimal
    fecha: datetime
    taller: Optional[str] = None
    proximo_km: Optional[int] = None
    proxima_fecha: Optional[date] = None


class MantenimientoCreate(MantenimientoBase):
    """Schema para crear Mantenimiento"""
    
    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        if v not in ["PREVENTIVO", "CORRECTIVO"]:
            raise ValueError("Tipo debe ser PREVENTIVO o CORRECTIVO")
        return v
    
    @field_validator("costo_bs")
    @classmethod
    def validar_costo(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("El costo debe ser mayor a 0")
        return v
    
    @field_validator("proximo_km")
    @classmethod
    def validar_proximo_km(cls, v: Optional[int]) -> Optional[int]:
        if v and v <= 0:
            raise ValueError("El próximo kilometraje debe ser mayor a 0")
        return v
    
    @field_validator("proxima_fecha")
    @classmethod
    def validar_proxima_fecha(cls, v: Optional[date]) -> Optional[date]:
        if v and v <= date.today():
            raise ValueError("La próxima fecha debe ser futura")
        return v


class MantenimientoUpdate(BaseModel):
    """Schema para actualizar Mantenimiento"""
    descripcion: Optional[str] = None
    costo_bs: Optional[Decimal] = None
    taller: Optional[str] = None
    proximo_km: Optional[int] = None
    proxima_fecha: Optional[date] = None


class MantenimientoResponse(MantenimientoBase):
    """Schema para respuesta de Mantenimiento"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Información del vehículo
    vehiculo_placa: Optional[str] = None
    vehiculo_marca: Optional[str] = None
    vehiculo_modelo: Optional[str] = None
    socio_nombre: Optional[str] = None
    
    # Propiedades calculadas
    costo_formateado: str
    es_preventivo: bool
    es_correctivo: bool
    tiene_programacion_siguiente: bool
    dias_hasta_proximo: Optional[int] = None
    mantenimiento_proximo: bool
    
    model_config = ConfigDict(from_attributes=True)


class MantenimientoReporte(BaseModel):
    """Schema para reporte de mantenimientos"""
    vehiculo_id: int
    vehiculo_placa: str
    vehiculo_identificacion: str
    socio_nombre: str
    mantenimientos_preventivos: int
    mantenimientos_correctivos: int
    costo_total: Decimal
    costo_promedio: Decimal
    ultimo_mantenimiento: Optional[datetime] = None
    proximo_mantenimiento: Optional[date] = None
    
    model_config = ConfigDict(from_attributes=True)


class AlertaMantenimiento(BaseModel):
    """Schema para alertas de mantenimiento"""
    vehiculo_id: int
    vehiculo_placa: str
    socio_nombre: str
    tipo_alerta: str  # VENCIMIENTO_DOCUMENTO, MANTENIMIENTO_DEBIDO
    descripcion: str
    fecha_vencimiento: Optional[date] = None
    dias_restantes: int
    prioridad: str  # ALTA, MEDIA, BAJA