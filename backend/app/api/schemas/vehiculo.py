from pydantic import ConfigDict, BaseModel, field_validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime, date


class VehiculoBase(BaseModel):
    """Schema base para Vehiculo"""
    placa: str
    marca: str
    modelo: str
    año: int
    capacidad_ton: Decimal
    socio_id: int
    estado: str = "ACTIVO"
    soat_vencimiento: Optional[date] = None
    itv_vencimiento: Optional[date] = None
    seguro_vencimiento: Optional[date] = None


class VehiculoCreate(VehiculoBase):
    """Schema para crear Vehiculo"""
    
    @field_validator("año")
    @classmethod
    def validar_año(cls, v: int) -> int:
        año_actual = datetime.now().year
        if v < 1990 or v > año_actual + 1:
            raise ValueError(f"Año debe estar entre 1990 y {año_actual + 1}")
        return v
    
    @field_validator("capacidad_ton")
    @classmethod
    def validar_capacidad(cls, v: Decimal) -> Decimal:
        if v <= 0 or v > 50:
            raise ValueError("Capacidad debe estar entre 0 y 50 toneladas")
        return v
    
    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: str) -> str:
        if v not in ["ACTIVO", "MANTENIMIENTO", "BAJA"]:
            raise ValueError("Estado debe ser ACTIVO, MANTENIMIENTO o BAJA")
        return v
    
    @field_validator("placa")
    @classmethod
    def validar_placa(cls, v: str) -> str:
        # Formato boliviano: ABC-1234
        if not v or len(v.replace("-", "")) < 6:
            raise ValueError("Placa debe tener formato válido")
        return v.upper()


class VehiculoUpdate(BaseModel):
    """Schema para actualizar Vehiculo"""
    marca: Optional[str] = None
    modelo: Optional[str] = None
    año: Optional[int] = None
    capacidad_ton: Optional[Decimal] = None
    socio_id: Optional[int] = None
    estado: Optional[str] = None
    soat_vencimiento: Optional[date] = None
    itv_vencimiento: Optional[date] = None
    seguro_vencimiento: Optional[date] = None
    
    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in ["ACTIVO", "MANTENIMIENTO", "BAJA"]:
            raise ValueError("Estado debe ser ACTIVO, MANTENIMIENTO o BAJA")
        return v


class RemolqueBase(BaseModel):
    """Schema base para Remolque"""
    placa: str
    tipo: str
    capacidad_ton: Decimal
    vehiculo_id: Optional[int] = None
    estado: str = "ACTIVO"


class RemolqueCreate(RemolqueBase):
    """Schema para crear Remolque"""
    pass


class RemolqueResponse(RemolqueBase):
    """Schema para respuesta de Remolque"""
    id: int
    created_at: datetime
    updated_at: datetime
    identificacion_completa: str
    
    model_config = ConfigDict(from_attributes=True)


class VehiculoResponse(VehiculoBase):
    """Schema para respuesta de Vehiculo"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Datos del socio
    socio_nombre: Optional[str] = None
    
    # Propiedades calculadas
    identificacion_completa: str
    documentos_vigentes: bool
    documentos_por_vencer: List[tuple]
    
    # Remolques asociados
    remolques: List[RemolqueResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class VehiculoReporte(BaseModel):
    """Schema para reporte de vehículo"""
    id: int
    placa: str
    marca: str
    modelo: str
    socio_nombre: str
    total_viajes: int
    km_recorridos: int
    costo_mantenimiento: Decimal
    tiempo_inactivo_dias: int
    rentabilidad: Decimal
    
    model_config = ConfigDict(from_attributes=True)


class DocumentoVencimiento(BaseModel):
    """Schema para documentos próximos a vencer"""
    vehiculo_id: int
    placa: str
    documento_tipo: str
    fecha_vencimiento: date
    dias_restantes: int
    socio_nombre: str