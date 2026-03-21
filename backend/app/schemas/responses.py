from pydantic import ConfigDict
"""
Responses estandarizadas para la API.
El Frontend siempre recibirá respuestas en este formato.
"""
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List, Dict, Any
from datetime import datetime

T = TypeVar('T')


class PaginationMeta(BaseModel):
    """Metadatos de paginación"""
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_prev: bool
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "total": 150,
                "page": 1,
                "limit": 20,
                "total_pages": 8,
                "has_next": True,
                "has_prev": False
            }
        })


class BaseResponse(BaseModel):
    """Respuesta base para operaciones simples"""
    success: bool = True
    message: Optional[str] = None
    # timestamp: datetime = None
    
    def __init__(self, **data):
        if 'timestamp' not in data or data['timestamp'] is None:
            data['timestamp'] = datetime.utcnow()
        super().__init__(**data)


class DataResponse(BaseResponse, Generic[T]):
    """Respuesta con datos de un único elemento"""
    data: T


class ListResponse(BaseResponse, Generic[T]):
    """Respuesta con lista de elementos (sin paginación)"""
    data: List[T]
    count: int = 0
    
    def __init__(self, **data):
        if 'count' not in data and 'data' in data:
            data['count'] = len(data['data'])
        super().__init__(**data)


class PaginatedResponse(BaseResponse, Generic[T]):
    """Respuesta paginada con estadísticas opcionales"""
    data: List[T]
    pagination: PaginationMeta
    estadisticas: Optional[Dict[str, Any]] = None
    filtros_aplicados: Optional[Dict[str, Any]] = None


class ErrorDetail(BaseModel):
    """Detalle de un error"""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None


class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    success: bool = False
    error: str
    code: str
    details: Optional[List[ErrorDetail]] = None
    # timestamp: datetime = None
    path: Optional[str] = None
    
    def __init__(self, **data):
        if 'timestamp' not in data or data['timestamp'] is None:
            data['timestamp'] = datetime.utcnow()
        super().__init__(**data)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "success": False,
                "error": "Viaje no encontrado",
                "code": "ENTITY_NOT_FOUND",
                "details": [
                    {"field": "id", "message": "No existe viaje con ID 999"}
                ],
                "timestamp": "2024-01-15T10:30:00Z",
                "path": "/api/v1/viajes/999"
            }
        }
    )

class ValidationErrorResponse(ErrorResponse):
    """Respuesta de error de validación"""
    code: str = "VALIDATION_ERROR"
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "success": False,
                "error": "Error de validación",
                "code": "VALIDATION_ERROR",
                "details": [
                    {"field": "peso_ton", "message": "El peso debe ser mayor a 0"},
                    {"field": "origen", "message": "El origen es requerido"}
                ]
            }
        }
    )

# ==================== VIAJES ====================

class ViajeBase(BaseModel):
    """Datos base de viaje"""
    cliente_id: int
    vehiculo_id: int
    chofer_id: int
    origen: str
    destino: str
    fecha_salida: datetime
    tipo_carga: str
    peso_ton: float
    km_estimado: int
    tarifa_tipo: str
    tarifa_valor: float
    notas: Optional[str] = None


class ViajeResumen(BaseModel):
    """Resumen de viaje para listados"""
    id: int
    ruta: str  # "Origen → Destino"
    cliente_nombre: str
    vehiculo_placa: str
    chofer_nombre: str
    fecha_salida: datetime
    estado: str
    ingreso_bs: float
    gastos_bs: float
    margen_bs: float
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "ruta": "La Paz → Santa Cruz",
                "cliente_nombre": "Empresa ABC",
                "vehiculo_placa": "1234-ABC",
                "chofer_nombre": "Juan Pérez",
                "fecha_salida": "2024-01-15T08:00:00Z",
                "estado": "EN_RUTA",
                "ingreso_bs": 15000.00,
                "gastos_bs": 3500.00,
                "margen_bs": 11500.00
            }
        })

class ViajeDetalle(ViajeResumen):
    """Detalle completo de viaje"""
    fecha_llegada: Optional[datetime]
    volumen_m3: Optional[float]
    km_real: Optional[int]
    notas: Optional[str]
    gastos: List["GastoViaje"] = []
    liquidacion: Optional["LiquidacionResumen"] = None
    created_at: datetime
    updated_at: datetime


class GastoViaje(BaseModel):
    """Gasto de viaje"""
    id: int
    tipo: str
    monto_bs: float
    descripcion: Optional[str]
    fecha: datetime


class LiquidacionResumen(BaseModel):
    """Resumen de liquidación"""
    id: int
    ingreso_bs: float
    gastos_bs: float
    pago_socio_bs: float
    saldo_socio_bs: float
    fecha: datetime


class EstadisticasViajes(BaseModel):
    """Estadísticas de viajes"""
    total_viajes: int
    ingresos_bs: float
    gastos_bs: float
    margen_bs: float
    rentabilidad_pct: float
    km_totales: int
    toneladas_totales: float
    por_estado: Dict[str, int]
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "total_viajes": 45,
                "ingresos_bs": 675000.00,
                "gastos_bs": 135000.00,
                "margen_bs": 540000.00,
                "rentabilidad_pct": 80.0,
                "km_totales": 25000,
                "toneladas_totales": 450.5,
                "por_estado": {
                    "PLANIFICADO": 5,
                    "EN_RUTA": 10,
                    "ENTREGADO": 20,
                    "LIQUIDADO": 10
                }
            }
        })


# ==================== DASHBOARD ====================

class DashboardResponse(BaseModel):
    """Respuesta del dashboard principal"""
    resumen_hoy: Dict[str, Any]
    resumen_mes: Dict[str, Any]
    viajes_recientes: List[ViajeResumen]
    alertas: List[Dict[str, Any]]
    graficos: Dict[str, List[Dict[str, Any]]]


# ==================== BÚSQUEDA GLOBAL ====================

class ResultadoBusqueda(BaseModel):
    """Resultado de búsqueda global"""
    tipo: str  # viaje, vehiculo, chofer, cliente, etc.
    id: int
    titulo: str
    subtitulo: str
    icono: str
    url: str


class BusquedaResponse(BaseModel):
    """Respuesta de búsqueda global"""
    query: str
    total_resultados: int
    resultados: List[ResultadoBusqueda]
    categorias: Dict[str, int]  # Conteo por categoría


# Resolver referencias forward
ViajeDetalle.model_rebuild()
