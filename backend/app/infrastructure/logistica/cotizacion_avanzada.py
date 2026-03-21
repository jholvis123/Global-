"""
ServicioCotizacionAvanzada: Cálculos de precio y análisis comercial
Integra los escenarios logísticos con tarificación y análisis de rentabilidad
"""
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from .logistica_service import LogisticaService, EscenarioCamion

@dataclass
class AnalisisComercial:
    """Resultado del análisis comercial de una ruta"""
    precio_por_tonelada: float
    precio_total_escenario_prom: float
    margen_operativo: float
    factor_rentabilidad: str  # "Alto", "Medio", "Bajo"
    dias_estimados: int
    
    def to_dict(self):
        return {
            "precio_por_tonelada": round(self.precio_por_tonelada, 2),
            "precio_total_escenario_promedio": round(self.precio_total_escenario_prom, 2),
            "margen_operativo_porcentaje": round(self.margen_operativo, 1),
            "rentabilidad": self.factor_rentabilidad,
            "dias_estimados": self.dias_estimados
        }

class ServicioCotizacionAvanzada:
    """
    Servicio de cotización integral que combina:
    - Análisis logístico (escenarios de carga)
    - Tarificación por ruta y tipo de carga
    - Análisis de rentabilidad comercial
    """
    
    def __init__(self, tarifa_repository):
        self.logistica = LogisticaService()
        self.tarifa_repo = tarifa_repository
        
        # Base de precios por kilómetro (USD)
        self.precios_base_km = {
            'LP': {'CBB': 2.20, 'SC': 1.80, 'PT': 2.50},
            'SC': {'LP': 1.80, 'CBB': 1.50, 'PT': 2.10},
            'CBB': {'LP': 2.50, 'SC': 1.50, 'PT': 2.00},
            'PT': {'LP': 2.50, 'SC': 2.10, 'CBB': 2.00}
        }
        
        # Distancias aproximadas (km)
        self.distancias_km = {
            ('LP', 'CBB'): 450,
            ('LP', 'SC'): 280,
            ('LP', 'PT'): 900,
            ('SC', 'LP'): 280,
            ('SC', 'CBB'): 220,
            ('SC', 'PT'): 650,
            ('CBB', 'LP'): 450,
            ('CBB', 'SC'): 220,
            ('CBB', 'PT'): 875,
            ('PT', 'LP'): 900,
            ('PT', 'SC'): 650,
            ('PT', 'CBB'): 875,
        }
        
        # Multiplicadores por tipo de carga
        self.multiplicadores_carga = {
            'general': 1.0,
            'peligrosa': 1.40,      # +40%
            'refrigerada': 1.25,    # +25%
            'fragil': 1.35,         # +35%
            'granel': 0.95          # -5% (volumen grande)
        }
    
    def cotizar_operacion_integral(
        self,
        toneladas: float,
        origen: str,
        destino: str,
        tipo_carga: str = "general",
        plazo_dias: Optional[int] = None
    ) -> Dict:
        """
        Cotiza una operación completa con análisis de 3 escenarios.
        
        Returns:
            Dict con cotización integral (escenarios + comercial)
        """
        
        # 1. Obtener escenarios logísticos
        escenarios = self.logistica.calcular_escenarios(toneladas, tipo_carga)
        
        # 2. Obtener distancia
        distancia = self._obtener_distancia(origen, destino)
        
        # 3. Calcular análisis comercial
        analisis = self._calcular_analisis_comercial(
            toneladas, 
            origen, 
            destino, 
            tipo_carga,
            distancia,
            plazo_dias or 5  # Por defecto 5 días
        )
        
        # 4. Cálculo de precios por escenario
        precios_escenarios = self._calcular_precios_escenarios(
            escenarios,
            analisis,
            toneladas
        )
        
        return {
            "carga_toneladas": toneladas,
            "ruta": {
                "origen": origen,
                "destino": destino,
                "distancia_km": distancia
            },
            "tipo_carga": tipo_carga,
            "escenarios_logisticos": {
                "conservador": escenarios['conservador'].to_dict(),
                "promedio": escenarios['promedio'].to_dict(),
                "optimo": escenarios['optimo'].to_dict()
            },
            "analisis_comercial": analisis.to_dict(),
            "precios_por_escenario": precios_escenarios,
            "recomendacion": self._generar_recomendacion(
                escenarios['promedio'],
                analisis,
                toneladas
            )
        }
    
    def _obtener_distancia(self, origen: str, destino: str) -> float:
        """Obtiene distancia de la matriz de rutas"""
        clave = (origen.upper(), destino.upper())
        return self.distancias_km.get(clave, 400)  # Default 400 km
    
    def _calcular_precio_base(
        self,
        origen: str,
        destino: str,
        tipo_carga: str,
        distancia: float
    ) -> float:
        """
        Calcula precio base considerando:
        - Distancia
        - Tipo de ruta
        - Tipo de carga (multiplicadores)
        """
        # Precio base por km
        precio_km = self.precios_base_km.get(origen, {}).get(destino, 2.0)
        
        # Precio por distancia
        precio_base = precio_km * distancia
        
        # Aplicar multiplicador por tipo de carga
        multiplicador = self.multiplicadores_carga.get(tipo_carga, 1.0)
        precio_final = precio_base * multiplicador
        
        return precio_final
    
    def _calcular_analisis_comercial(
        self,
        toneladas: float,
        origen: str,
        destino: str,
        tipo_carga: str,
        distancia: float,
        plazo_dias: int
    ) -> AnalisisComercial:
        """Analiza factibilidad y rentabilidad de la operación"""
        
        precio_total = self._calcular_precio_base(
            origen, destino, tipo_carga, distancia
        )
        
        precio_por_ton = precio_total / toneladas
        
        # Margen operativo (simulado)
        # Operaciones largas: mayor margen
        margen_base = 25 if distancia > 500 else 20
        multiplicador_plazo = 1.1 if plazo_dias <= 3 else 0.95
        margen_operativo = margen_base * multiplicador_plazo
        
        # Clasificación de rentabilidad
        if margen_operativo >= 28:
            rentabilidad = "Alto"
        elif margen_operativo >= 20:
            rentabilidad = "Medio"
        else:
            rentabilidad = "Bajo"
        
        return AnalisisComercial(
            precio_por_tonelada=precio_por_ton,
            precio_total_escenario_prom=precio_total,
            margen_operativo=margen_operativo,
            factor_rentabilidad=rentabilidad,
            dias_estimados=plazo_dias
        )
    
    def _calcular_precios_escenarios(
        self,
        escenarios: Dict[str, EscenarioCamion],
        analisis: AnalisisComercial,
        toneladas: float
    ) -> Dict:
        """Calcula precio total para cada escenario"""
        
        precio_tonelada = analisis.precio_por_tonelada
        
        return {
            "conservador": round(toneladas * precio_tonelada * 1.10, 2),   # +10%
            "promedio": round(toneladas * precio_tonelada, 2),             # Base
            "optimo": round(toneladas * precio_tonelada * 0.95, 2)        # -5%
        }
    
    def _generar_recomendacion(
        self,
        escenario_prom: EscenarioCamion,
        analisis: AnalisisComercial,
        toneladas: float
    ) -> str:
        """Genera recomendación profesional de cómo proceder"""
        
        recomendacion = []
        
        recomendacion.append(
            f"Para transportar {toneladas:,.0f} toneladas, "
            f"le recomendamos {escenario_prom.cantidad_camiones} unidades "
            f"(escenario promedio)."
        )
        
        if analisis.factor_rentabilidad == "Alto":
            recomendacion.append(
                "Esta operación presenta márgenes muy atractivos. "
                "Considere incluso el escenario óptimo para mayor rentabilidad."
            )
        elif analisis.factor_rentabilidad == "Medio":
            recomendacion.append(
                "Operación estable con rentabilidad adecuada. "
                "El escenario promedio es la opción más balanceada."
            )
        else:
            recomendacion.append(
                "Operación viable pero con márgenes ajustados. "
                "Analice costos variables antes de confirmar."
            )
        
        recomendacion.append(
            f"Plazo estimado: {analisis.dias_estimados} días. "
            f"¿Desea confirmar esta operación o explorar alternativas?"
        )
        
        return " ".join(recomendacion)


if __name__ == "__main__":
    # Test básico
    from backend.app.db.database import SessionLocal
    
    session = SessionLocal()
    
    class MockTarifaRepo:
        pass
    
    servicio = ServicioCotizacionAvanzada(MockTarifaRepo())
    
    resultado = servicio.cotizar_operacion_integral(
        toneladas=500,
        origen="LP",
        destino="CBB",
        tipo_carga="general"
    )
    
    import json
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
