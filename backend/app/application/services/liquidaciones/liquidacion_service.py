"""
Services - Liquidaciones
"""
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from decimal import Decimal

from app.core.unit_of_work import UnitOfWork
from app.domain.exceptions import (
    EntityNotFoundException,
    BusinessRuleException
)
from app.domain.services import CalculadoraLiquidacion


class LiquidacionService:
    """Servicio de aplicación para gestión de liquidaciones"""
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.calculadora = CalculadoraLiquidacion()
    
    def listar(
        self,
        page: int = 1,
        limit: int = 20,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """Listar liquidaciones con filtros"""
        with self.uow:
            if fecha_inicio and fecha_fin:
                liquidaciones = self.uow.liquidaciones.get_by_periodo(
                    fecha_inicio, fecha_fin
                )
                total = len(liquidaciones)
            else:
                liquidaciones = self.uow.liquidaciones.get_all(
                    skip=(page - 1) * limit,
                    limit=limit
                )
                total = self.uow.liquidaciones.count()
            
            return {
                "data": [self._to_dict(l) for l in liquidaciones],
                "total": total,
                "page": page,
                "limit": limit
            }
    
    def obtener(self, liquidacion_id: int) -> Dict[str, Any]:
        """Obtener detalle de liquidación"""
        with self.uow:
            liquidacion = self.uow.liquidaciones.get_with_viaje(liquidacion_id)
            if not liquidacion:
                raise EntityNotFoundException("Liquidación", liquidacion_id)
            return self._to_dict(liquidacion, completo=True)
    
    def generar(self, viaje_id: int, usuario_id: int) -> Dict[str, Any]:
        """Generar liquidación para un viaje"""
        with self.uow:
            # Obtener viaje
            viaje = self.uow.viajes.get_with_relations(viaje_id)
            if not viaje:
                raise EntityNotFoundException("Viaje", viaje_id)
            
            if viaje.estado != "ENTREGADO":
                raise BusinessRuleException("Solo viajes ENTREGADOS pueden liquidarse")
            
            # Verificar no existe liquidación
            existente = self.uow.liquidaciones.get_by_viaje(viaje_id)
            if existente:
                raise BusinessRuleException("El viaje ya tiene liquidación")
            
            # Obtener socio del vehículo
            socio = viaje.vehiculo.socio if viaje.vehiculo else None
            if not socio:
                raise BusinessRuleException("El vehículo no tiene socio asignado")
            
            # Obtener anticipos pendientes del chofer
            anticipos_total = self.uow.anticipos.get_total_pendiente_chofer(viaje.chofer_id)
            
            # Calcular liquidación
            gastos = [{"tipo": g.tipo, "monto_bs": float(g.monto_bs)} for g in viaje.gastos]
            calculo = self.calculadora.calcular(
                ingreso_bs=Decimal(str(viaje.ingreso_total_bs)),
                gastos=gastos,
                porcentaje_socio=Decimal(str(socio.porcentaje_participacion)),
                anticipos_pendientes=anticipos_total
            )
            
            # Crear liquidación
            liquidacion = self.uow.liquidaciones.create({
                "viaje_id": viaje_id,
                "ingreso_bs": calculo["ingreso_bs"],
                "gastos_bs": calculo["gastos_bs"],
                "pago_socio_bs": calculo["pago_socio_bs"],
                "saldo_socio_bs": calculo["saldo_socio_bs"],
                "fecha": datetime.utcnow()
            })
            
            # Actualizar estado del viaje
            self.uow.viajes.update(viaje_id, {"estado": "LIQUIDADO"})
            
            # Marcar anticipos como descontados
            anticipos = self.uow.anticipos.get_pendientes_chofer(viaje.chofer_id)
            for anticipo in anticipos:
                self.uow.anticipos.marcar_descontado(anticipo.id, viaje_id)
            
            self.uow.commit()
            
            return {
                **self._to_dict(liquidacion),
                "calculo_detalle": calculo
            }
    
    def obtener_pendientes(self) -> List[Dict[str, Any]]:
        """Obtener viajes pendientes de liquidación"""
        with self.uow:
            viajes = self.uow.viajes.get_viajes_pendientes_liquidacion()
            return [{
                "id": v.id,
                "ruta": f"{v.origen} → {v.destino}",
                "fecha_salida": str(v.fecha_salida),
                "ingreso_bs": float(v.ingreso_total_bs),
                "gastos_bs": float(v.total_gastos_bs)
            } for v in viajes]
    
    def _to_dict(self, l, completo: bool = False) -> Dict[str, Any]:
        """Convertir entidad a diccionario"""
        data = {
            "id": l.id,
            "viaje_id": l.viaje_id,
            "ingreso_bs": float(l.ingreso_bs),
            "gastos_bs": float(l.gastos_bs),
            "pago_socio_bs": float(l.pago_socio_bs),
            "saldo_socio_bs": float(l.saldo_socio_bs),
            "fecha": str(l.fecha)
        }
        if completo and l.viaje:
            data["viaje"] = {
                "ruta": f"{l.viaje.origen} → {l.viaje.destino}",
                "cliente": l.viaje.cliente.nombre if l.viaje.cliente else None
            }
        return data
