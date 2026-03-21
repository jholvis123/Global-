from abc import ABC, abstractmethod
from app.domain.chatbot.entities import TipoCarga

class EstrategiaCalculoTarifa(ABC):
    @abstractmethod
    def calcular(self, precio_base_ruta: float, peso_kg: float) -> float:
        pass

class CalculoCargaGeneral(EstrategiaCalculoTarifa):
    def calcular(self, precio_base_ruta: float, peso_kg: float) -> float:
        return precio_base_ruta + (peso_kg * 0.5)

class CalculoCargaPeligrosa(EstrategiaCalculoTarifa):
    def calcular(self, precio_base_ruta: float, peso_kg: float) -> float:
        costo_base_peso = precio_base_ruta + (peso_kg * 0.8)
        return costo_base_peso * 1.5

class CalculoCargaRefrigerada(EstrategiaCalculoTarifa):
    def calcular(self, precio_base_ruta: float, peso_kg: float) -> float:
        costo_base_peso = precio_base_ruta + (peso_kg * 0.6)
        return costo_base_peso * 1.3

class FabricaEstrategiasTarifa:
    """Fábrica que determina la estrategia correcta en base al tipo de carga"""
    
    @staticmethod
    def obtener_estrategia(tipo_carga: TipoCarga) -> EstrategiaCalculoTarifa:
        estrategias = {
            TipoCarga.GENERAL: CalculoCargaGeneral(),
            TipoCarga.PELIGROSA: CalculoCargaPeligrosa(),
            TipoCarga.REFRIGERADA: CalculoCargaRefrigerada(),
        }
        return estrategias.get(tipo_carga, CalculoCargaGeneral())
