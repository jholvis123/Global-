from pydantic import ConfigDict, BaseModel
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import date, datetime


class ReporteDiario(BaseModel):
    """Schema para reporte diario"""
    fecha: date
    total_viajes: int
    ingresos_bs: Decimal
    gastos_bs: Decimal
    ganancia_bs: Decimal
    rentabilidad_porcentaje: float
    viajes_por_estado: Dict[str, int]
    tipos_carga: Dict[str, int]
    
    model_config = ConfigDict(from_attributes=True)


class ReporteMensual(BaseModel):
    """Schema para reporte mensual"""
    año: int
    mes: int
    nombre_mes: str
    total_viajes: int
    ingresos_bs: Decimal
    gastos_bs: Decimal
    ganancia_bs: Decimal
    rentabilidad_porcentaje: float
    dias_laborables: int
    promedio_diario: Decimal
    comparacion_mes_anterior: Optional[Dict[str, float]] = None
    
    model_config = ConfigDict(from_attributes=True)


class ReporteTipoCarga(BaseModel):
    """Schema para reporte por tipo de carga"""
    tipo_carga: str
    total_viajes: int
    peso_total_ton: Decimal
    ingreso_total_bs: Decimal
    gasto_total_bs: Decimal
    margen_bs: Decimal
    rentabilidad_porcentaje: float
    precio_promedio_ton: Decimal
    
    model_config = ConfigDict(from_attributes=True)


class ReporteResumen(BaseModel):
    """Schema para reporte resumen"""
    periodo_inicio: date
    periodo_fin: date
    total_viajes: int
    total_ingresos: Decimal
    total_gastos: Decimal
    ganancia_neta: Decimal
    rentabilidad_general: float
    
    # Desglose por categorías
    por_tipo_carga: List[ReporteTipoCarga]
    por_socio: List[Dict[str, Any]]
    por_chofer: List[Dict[str, Any]]
    por_vehiculo: List[Dict[str, Any]]
    
    # KPIs
    viaje_mas_rentable: Optional[Dict[str, Any]] = None
    viaje_menos_rentable: Optional[Dict[str, Any]] = None
    socio_mas_productivo: Optional[Dict[str, Any]] = None
    chofer_mas_activo: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(from_attributes=True)


class ReporteSocio(BaseModel):
    """Schema para reporte individual de socio"""
    socio_id: int
    socio_nombre: str
    periodo_inicio: date
    periodo_fin: date
    
    # Estadísticas generales
    vehiculos_activos: int
    total_viajes: int
    ingresos_generados: Decimal
    gastos_operativos: Decimal
    margen_bruto: Decimal
    
    # Participaciones y anticipos
    participacion_configurada: Decimal
    pago_total_recibido: Decimal
    anticipos_otorgados: Decimal
    saldo_pendiente: Decimal
    
    # Desglose por vehículo
    detalle_vehiculos: List[Dict[str, Any]]
    
    # Análisis temporal
    ingresos_mensuales: List[Dict[str, Any]]
    
    model_config = ConfigDict(from_attributes=True)


class ReporteChofer(BaseModel):
    """Schema para reporte individual de chofer"""
    chofer_id: int
    chofer_nombre: str
    periodo_inicio: date
    periodo_fin: date
    
    # Estadísticas de actividad
    total_viajes: int
    km_recorridos: int
    dias_trabajados: int
    promedio_viajes_mes: float
    
    # Estadísticas financieras
    viaticos_recibidos: Decimal
    gastos_rendidos: Decimal
    anticipos_recibidos: Decimal
    saldo_pendiente: Decimal
    
    # Rendimiento
    puntualidad_porcentaje: float
    viajes_completados_tiempo: int
    incidencias_reportadas: int
    
    # Desglose por tipo de carga
    experiencia_cargas: List[Dict[str, Any]]
    
    model_config = ConfigDict(from_attributes=True)


class FiltrosReporte(BaseModel):
    """Schema para filtros de reportes"""
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    cliente_id: Optional[int] = None
    socio_id: Optional[int] = None
    chofer_id: Optional[int] = None
    vehiculo_id: Optional[int] = None
    tipo_carga: Optional[str] = None
    estado_viaje: Optional[str] = None
    
    # Paginación
    page: int = 1
    size: int = 50
    
    # Ordenamiento
    sort_by: str = "fecha_salida"
    sort_order: str = "desc"


class ExportRequest(BaseModel):
    """Schema para solicitud de exportación"""
    tipo_reporte: str  # diario, mensual, resumen, socio, chofer
    formato: str  # pdf, xlsx
    filtros: FiltrosReporte
    incluir_graficos: bool = True
    idioma: str = "es"