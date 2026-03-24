from pydantic import ConfigDict, BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


class LiquidacionBase(BaseModel):
    """Schema base para Liquidacion"""
    viaje_id: int
    ingreso_bs: Decimal
    gastos_bs: Decimal
    pago_socio_bs: Decimal
    saldo_socio_bs: Decimal
    saldo_chofer_bs: Decimal = Decimal("0.00")
    fecha: datetime


class LiquidacionCreate(LiquidacionBase):
    """Schema para crear Liquidacion"""
    pass


class LiquidacionResponse(LiquidacionBase):
    """Schema para respuesta de Liquidacion"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Propiedades calculadas
    margen_bs: float
    ingreso_formateado: str
    gastos_formateados: str
    margen_formateado: str
    pago_socio_formateado: str
    saldo_socio_formateado: str
    rentabilidad_porcentaje: float
    
    # Información del viaje
    viaje_origen: Optional[str] = None
    viaje_destino: Optional[str] = None
    viaje_fecha_salida: Optional[datetime] = None
    viaje_tipo_carga: Optional[str] = None
    
    # Información del socio y chofer
    socio_nombre: Optional[str] = None
    chofer_nombre: Optional[str] = None
    vehiculo_placa: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class ResumenLiquidacion(BaseModel):
    """Schema para resumen de liquidaciones"""
    periodo: str
    total_viajes: int
    total_ingresos: Decimal
    total_gastos: Decimal
    total_margen: Decimal
    rentabilidad_promedio: float
    mejor_viaje: Optional[dict] = None
    peor_viaje: Optional[dict] = None
    
    model_config = ConfigDict(from_attributes=True)