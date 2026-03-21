from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from app.domain.chatbot.entities import Tarifa, SolicitudCotizacion

class RepositorioTarifas(ABC):
    """Interfaz abstracta para aislar el acceso a la base de datos"""
    
    @abstractmethod
    def buscar_tarifa(self, origen: str, destino: str) -> Optional[Tarifa]:
        pass

    @abstractmethod
    def guardar_solicitud(self, solicitud: SolicitudCotizacion) -> SolicitudCotizacion:
        pass

class ServicioPLN(ABC):
    """Interfaz abstracta para aislar el motor de lenguaje natural"""
    
    @abstractmethod
    def extraer_datos_cotizacion(self, texto: str) -> Dict[str, Any]:
        """Extrae: origen, destino, tipo_carga, peso_kg del string en lenguaje natural"""
        pass
