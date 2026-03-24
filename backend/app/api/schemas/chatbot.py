from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Optional, List
from app.domain.chatbot.entities import TipoCarga

class CotizacionRequest(BaseModel):
    mensaje_texto: str = Field(..., description="Mensaje natural del usuario. Ej: 'Necesito llevar 500kg de manzanas desde Santa Cruz a La Paz'")

class CotizacionResponse(BaseModel):
    id_solicitud: int
    origen: str
    destino: str
    peso_kg: float
    tipo_carga: TipoCarga
    precio_cotizado_bs: float
    fecha: datetime


# === ESQUEMAS AVANZADOS (Phase 3) ===

class EscenarioCamionSchema(BaseModel):
    """Representa un escenario de carga"""
    capacidad_por_camion: float
    cantidad_camiones: int
    carga_total: float
    utilizacion_porcentaje: float
    descripcion: str


class AnalisisComercialSchema(BaseModel):
    """Análisis comercial de la operación"""
    precio_por_tonelada: float
    precio_total_escenario_promedio: float
    margen_operativo_porcentaje: float
    rentabilidad: str
    dias_estimados: int


class RutaSchema(BaseModel):
    """Información de ruta"""
    origen: str
    destino: str
    distancia_km: int


class CotizacionAvanzadaRequest(BaseModel):
    """Solicitud avanzada de cotización (toneladas)"""
    mensaje_texto: str = Field(..., description="Mensaje con toneladas, origen, destino")
    

class CotizacionAvanzadaResponse(BaseModel):
    """Respuesta avanzada con múltiples escenarios"""
    carga_toneladas: float
    ruta: RutaSchema
    tipo_carga: str
    escenarios_logisticos: Dict[str, EscenarioCamionSchema]
    analisis_comercial: AnalisisComercialSchema
    precios_por_escenario: Dict[str, float]
    recomendacion: str
    respuesta_profesional: Optional[str] = None  # Formato de 4 secciones


# === ESQUEMAS DE CONVERSACIÓN (OpenAI GPT) ===

class MensajeSchema(BaseModel):
    """Un mensaje individual en la conversación"""
    role: str = Field(..., description="'user' o 'assistant'")
    content: str = Field(..., description="Contenido del mensaje")

class ConversacionRequest(BaseModel):
    """Solicitud de conversación con historial"""
    mensaje: str = Field(..., description="Mensaje actual del usuario", min_length=1)
    historial: Optional[List[MensajeSchema]] = Field(default=[], description="Historial de la conversación")

class ConversacionResponse(BaseModel):
    """Respuesta de conversación con metadatos"""
    respuesta: str = Field(..., description="Respuesta del bot en lenguaje natural")
    requiere_cotizacion: bool = Field(default=False, description="Si GPT detectó datos suficientes para cotizar")
    datos_extraidos: Optional[Dict] = Field(default=None, description="Datos de cotización extraídos, si los hay")
    cotizacion_avanzada: Optional[CotizacionAvanzadaResponse] = Field(default=None, description="Cotización generada si requiere_cotizacion=true")

