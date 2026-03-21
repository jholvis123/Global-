from typing import Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field

class TipoCarga(str, Enum):
    GENERAL = "general"
    PELIGROSA = "peligrosa"
    REFRIGERADA = "refrigerada"
    FRAGIL = "fragil"

class ZonaGeografica(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    tarifa_base_km: float

class Tarifa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    zona_origen_id: int = Field(foreign_key="zonageografica.id")
    zona_destino_id: int = Field(foreign_key="zonageografica.id")
    distancia_km: float
    precio_base: float

class SolicitudCotizacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    texto_original: str
    fecha_solicitud: datetime = Field(default_factory=datetime.utcnow)
    origen: str
    destino: str
    tipo_carga: TipoCarga
    peso_kg: float
    precio_calculado: Optional[float] = None
