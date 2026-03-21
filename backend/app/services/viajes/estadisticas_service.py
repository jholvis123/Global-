"""
Services - Viajes (Estadísticas y Dashboard)
"""
from typing import Dict, Any, List
from datetime import date
from decimal import Decimal

from app.core.unit_of_work import UnitOfWork
from app.domain.services import CalculadoraEstadisticas


class ViajeEstadisticasService:
    """Servicio para estadísticas de viajes"""
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.calculadora = CalculadoraEstadisticas()
    
    def dashboard(self) -> Dict[str, Any]:
        """Obtener datos para dashboard principal"""
        with self.uow:
            hoy = date.today()
            
            # Contadores rápidos
            planificados = len(self.uow.viajes.get_by_estado("PLANIFICADO"))
            en_ruta = len(self.uow.viajes.get_by_estado("EN_RUTA"))
            pendientes = len(self.uow.viajes.get_viajes_pendientes_liquidacion())
            
            # Estadísticas del mes
            mes_stats = self.uow.viajes.get_estadisticas_mensuales(hoy.year, hoy.month)
            
            # Vehículos disponibles
            vehiculos_disponibles = len(self.uow.vehiculos.get_disponibles())
            vehiculos_en_mant = len(self.uow.vehiculos.get_en_mantenimiento())
            
            # Alertas
            alertas = self._generar_alertas()
            
            return {
                "contadores": {
                    "viajes_planificados": planificados,
                    "viajes_en_ruta": en_ruta,
                    "pendientes_liquidacion": pendientes,
                    "vehiculos_disponibles": vehiculos_disponibles,
                    "vehiculos_mantenimiento": vehiculos_en_mant
                },
                "mes_actual": mes_stats,
                "alertas": alertas
            }
    
    def resumen_periodo(
        self, 
        fecha_inicio: date, 
        fecha_fin: date
    ) -> Dict[str, Any]:
        """Resumen de un período específico"""
        with self.uow:
            # Obtener viajes del período
            viajes = self.uow.viajes.get_all(
                filters={
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
            )
            
            viajes_data = [{
                "ingreso_bs": float(v.ingreso_total_bs),
                "gastos_bs": float(v.total_gastos_bs),
                "peso_ton": float(v.peso_ton),
                "km_estimado": v.km_estimado,
                "km_real": v.km_real,
                "estado": v.estado
            } for v in viajes]
            
            return self.calculadora.calcular_resumen_viajes(viajes_data)
    
    def _generar_alertas(self) -> List[Dict[str, Any]]:
        """Generar alertas del sistema"""
        alertas = []
        
        # Vehículos con documentos por vencer
        from datetime import timedelta
        fecha_limite = date.today() + timedelta(days=30)
        vehiculos_vencidos = self.uow.vehiculos.get_con_documentos_vencidos(fecha_limite)
        
        for v in vehiculos_vencidos:
            alertas.append({
                "tipo": "warning",
                "titulo": "Documento por vencer",
                "mensaje": f"SOAT del vehículo {v.placa} vence pronto",
                "entidad": "vehiculo",
                "entidad_id": v.id
            })
        
        # Choferes con licencia vencida
        choferes_vencidos = self.uow.choferes.get_con_licencia_vencida()
        for c in choferes_vencidos:
            alertas.append({
                "tipo": "error",
                "titulo": "Licencia vencida",
                "mensaje": f"Licencia de {c.nombre} {c.apellido} está vencida",
                "entidad": "chofer",
                "entidad_id": c.id
            })
        
        # Mantenimientos próximos
        mant_proximos = self.uow.mantenimientos.get_proximos(7)
        for m in mant_proximos:
            alertas.append({
                "tipo": "info",
                "titulo": "Mantenimiento programado",
                "mensaje": f"Mantenimiento programado próximamente",
                "entidad": "mantenimiento",
                "entidad_id": m.id
            })
        
        return alertas
