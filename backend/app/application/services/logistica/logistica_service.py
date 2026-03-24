"""
LogisticaService: Cálculos operativos de escenarios de carga
Analiza cuántos camiones se necesitan considerando diferentes capacidades
"""
import math
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class CapacidadCamion(Enum):
    """Capacidades operativas de camiones disponibles"""
    CONSERVADOR = 26.0       # Camiones antiguos, carga parcial
    CONSERVADOR_MEDIO = 27.0 # Transición
    PROMEDIO = 27.5          # Operativo estándar
    OPTIMO = 28.5            # Máxima capacidad (semirremolque completo)

@dataclass
class EscenarioCamion:
    """Resultado del análisis de un escenario"""
    capacidad_por_camion: float
    cantidad_camiones: int
    descarga_total_real: float
    utilization_percentage: float
    descripcion_operativa: str
    
    def to_dict(self):
        return {
            "capacidad_por_camion": self.capacidad_por_camion,
            "cantidad_camiones": self.cantidad_camiones,
            "carga_total": self.descarga_total_real,
            "utilizacion_porcentaje": round(self.utilization_percentage, 1),
            "descripcion": self.descripcion_operativa
        }

class LogisticaService:
    """
    Servicio especializado en análisis logístico de transporte de carga.
    Calcula automáticamente escenarios eficientes de carga.
    """
    
    def __init__(self):
        # Descripciones operativas por escenario
        self.descripciones = {
            26.0: "Escenario Conservador - Camiones con carga parcial",
            27.0: "Escenario Conservador-Medio - Carga moderada",
            27.5: "Escenario Promedio - Operativo estándar recomendado",
            28.5: "Escenario Óptimo - Máxima rentabilidad operativa"
        }
    
    def calcular_escenarios(
        self, 
        toneladas_totales: float,
        tipo_carga: Optional[str] = None
    ) -> Dict[str, EscenarioCamion]:
        """
        Calcula los tres escenarios principales de carga.
        
        Args:
            toneladas_totales: Cantidad total a transportar
            tipo_carga: Tipo de carga (afecta capacidad real)
        
        Returns:
            Dict con escenarios: conservador, promedio, optimo
        """
        
        # Ajustar capacidades según tipo de carga
        factor_capacidad = self._get_factor_capacidad(tipo_carga)
        
        escenarios = {}
        
        # ESCENARIO CONSERVADOR
        escenarios['conservador'] = self._calcular_escenario(
            toneladas_totales,
            CapacidadCamion.CONSERVADOR.value * factor_capacidad,
            "Conservador - Para operaciones con restricciones o flota limitada"
        )
        
        # ESCENARIO PROMEDIO (RECOMENDADO)
        escenarios['promedio'] = self._calcular_escenario(
            toneladas_totales,
            CapacidadCamion.PROMEDIO.value * factor_capacidad,
            "Promedio - Le recomendamos este escenario para optimizar operación"
        )
        
        # ESCENARIO ÓPTIMO
        escenarios['optimo'] = self._calcular_escenario(
            toneladas_totales,
            CapacidadCamion.OPTIMO.value * factor_capacidad,
            "Óptimo - Máxima eficiencia si dispone de flota capacitada"
        )
        
        return escenarios
    
    def _calcular_escenario(
        self,
        toneladas_totales: float,
        capacidad_real_por_camion: float,
        descripcion: str
    ) -> EscenarioCamion:
        """Calcula detalles de un escenario específico"""
        
        cantidad_camiones = math.ceil(toneladas_totales / capacidad_real_por_camion)
        carga_total_real = cantidad_camiones * capacidad_real_por_camion
        utilizacion = (toneladas_totales / carga_total_real * 100) if carga_total_real > 0 else 0
        
        return EscenarioCamion(
            capacidad_por_camion=round(capacidad_real_por_camion, 1),
            cantidad_camiones=cantidad_camiones,
            descarga_total_real=round(carga_total_real, 1),
            utilization_percentage=utilizacion,
            descripcion_operativa=descripcion
        )
    
    def _get_factor_capacidad(self, tipo_carga: Optional[str]) -> float:
        """
        Retorna factor multiplicador según tipo de carga.
        Algunos tipos reducen la capacidad real del camión.
        """
        factores = {
            'general': 1.0,        # Sin restricciones
            'granel': 0.95,        # Polvo/granel: -5% (espacio)
            'peligrosa': 0.85,     # Químicos: -15% (norma de seguridad)
            'refrigerada': 0.90,   # Congelado: -10% (sistema frigorífico)
            'fragil': 0.80,        # Vidrio/frágil: -20% (cuidado)
            'contenedor': 1.0      # Contenedores: capacidad normal
        }
        return factores.get(tipo_carga if tipo_carga else 'general', 1.0)
    
    def estimar_tiempo_transito(
        self,
        distancia_km: float,
        velocidad_promedio_kmh: float = 60,
        horas_descanso: float = 0
    ) -> Dict[str, float]:
        """
        Estima tiempo de tránsito considerando:
        - Distancia
        - Velocidad promedio
        - Descansos obligatorios
        """
        horas_manejo = distancia_km / velocidad_promedio_kmh
        horas_totales = horas_manejo + horas_descanso
        dias = horas_totales / 24
        
        return {
            "horas_manejo": round(horas_manejo, 1),
            "horas_descanso": horas_descanso,
            "horas_totales": round(horas_totales, 1),
            "dias_estimado": round(dias, 1)
        }
    
    def generar_reporte_logistico(
        self,
        toneladas: float,
        escenarios: Dict[str, EscenarioCamion],
        distancia_km: float,
        ruta_origen: str,
        ruta_destino: str,
        tipo_carga: str = "general"
    ) -> str:
        """
        Genera un reporte profesional de análisis logístico.
        """
        escenario_prom = escenarios['promedio']
        tiempo = self.estimar_tiempo_transito(distancia_km)
        
        reporte = f"""
╔════════════════════════════════════════════════════════════════╗
║                  ANÁLISIS LOGÍSTICO OPERATIVO                ║
╚════════════════════════════════════════════════════════════════╝

📍 RUTA SOLICITADA:
   Origen: {ruta_origen}
   Destino: {ruta_destino}
   Distancia: {distancia_km} km
   Tipo de Carga: {tipo_carga.upper()}

📦 CARGA TOTAL A TRANSPORTAR: {toneladas:,.0f} toneladas

🚚 ESTIMACIÓN DE UNIDADES NECESARIAS:

   • ESCENARIO CONSERVADOR:
     - Capacidad por camión: {escenarios['conservador'].capacidad_por_camion} ton
     - Unidades necesarias: {escenarios['conservador'].cantidad_camiones} camiones
     - Utilización: {escenarios['conservador'].utilization_percentage:.1f}%
     
   • ESCENARIO PROMEDIO (Recomendado):
     - Capacidad por camión: {escenarios['promedio'].capacidad_por_camion} ton
     - Unidades necesarias: {escenarios['promedio'].cantidad_camiones} camiones
     - Utilización: {escenarios['promedio'].utilization_percentage:.1f}%
     
   • ESCENARIO ÓPTIMO:
     - Capacidad por camión: {escenarios['optimo'].capacidad_por_camion} ton
     - Unidades necesarias: {escenarios['optimo'].cantidad_camiones} camiones
     - Utilización: {escenarios['optimo'].utilization_percentage:.1f}%

⏱️  TIEMPO ESTIMADO DE TRÁNSITO:
   - Tiempo de manejo: {tiempo['horas_manejo']} horas
   - Tiempo total: {tiempo['horas_totales']} horas ({tiempo['dias_estimado']} días)

✅ RECOMENDACIÓN OPERATIVA:
   Para esta operación de {toneladas:,.0f} toneladas, consideramos
   optimal el escenario promedio con {escenario_prom.cantidad_camiones} unidades.
   Esto balancear rentabilidad y disponibilidad de flota.

   ¿Desea continuar con una cotización de precios o analizar
   otro aspecto de la operación?
"""
        return reporte

if __name__ == "__main__":
    # Test del servicio
    servicio = LogisticaService()
    
    escenarios = servicio.calcular_escenarios(1000, "general")
    
    for nombre, escenario in escenarios.items():
        print(f"{nombre}: {escenario.cantidad_camiones} camiones")
