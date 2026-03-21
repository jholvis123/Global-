"""
Services - Anticipos
"""
from typing import Optional, List, Dict, Any
from datetime import date
from decimal import Decimal

from app.core.unit_of_work import UnitOfWork
from app.domain.exceptions import (
    EntityNotFoundException,
    BusinessRuleException
)
from app.domain.value_objects import Dinero


class AnticipoService:
    """Servicio de aplicación para gestión de anticipos"""
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    def listar(
        self,
        page: int = 1,
        limit: int = 20,
        chofer_id: Optional[int] = None,
        estado: Optional[str] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """Listar anticipos con filtros"""
        with self.uow:
            filtros = {}
            if chofer_id:
                filtros["chofer_id"] = chofer_id
            if estado:
                filtros["estado"] = estado
            
            anticipos = self.uow.anticipos.get_all(
                skip=(page - 1) * limit,
                limit=limit,
                filters=filtros
            )
            total = self.uow.anticipos.count(filtros)
            
            # Calcular totales
            total_bs = sum(float(a.monto_bs) for a in anticipos)
            
            return {
                "data": [self._to_dict(a) for a in anticipos],
                "total": total,
                "page": page,
                "limit": limit,
                "estadisticas": {
                    "total_bs": total_bs
                }
            }
    
    def obtener(self, anticipo_id: int) -> Dict[str, Any]:
        """Obtener detalle de anticipo"""
        with self.uow:
            anticipo = self.uow.anticipos.get_by_id(anticipo_id)
            if not anticipo:
                raise EntityNotFoundException("Anticipo", anticipo_id)
            return self._to_dict(anticipo, completo=True)
    
    def crear(self, datos: Dict[str, Any], usuario_id: int) -> Dict[str, Any]:
        """Crear nuevo anticipo"""
        with self.uow:
            # Validar chofer existe
            chofer = self.uow.choferes.get_by_id(datos["chofer_id"])
            if not chofer:
                raise EntityNotFoundException("Chofer", datos["chofer_id"])
            
            # Validar monto positivo
            monto = Decimal(str(datos["monto_bs"]))
            if monto <= 0:
                raise BusinessRuleException("El monto debe ser mayor a 0")
            
            anticipo = self.uow.anticipos.create({
                **datos,
                "estado": "PENDIENTE",
                "fecha": datos.get("fecha", date.today()),
                "creado_por": usuario_id
            })
            self.uow.commit()
            
            return self._to_dict(anticipo)
    
    def eliminar(self, anticipo_id: int) -> bool:
        """Eliminar anticipo"""
        with self.uow:
            anticipo = self.uow.anticipos.get_by_id(anticipo_id)
            if not anticipo:
                raise EntityNotFoundException("Anticipo", anticipo_id)
            
            if anticipo.estado == "DESCONTADO":
                raise BusinessRuleException("No se puede eliminar un anticipo descontado")
            
            self.uow.anticipos.delete(anticipo_id)
            self.uow.commit()
            return True
    
    def obtener_pendientes_chofer(self, chofer_id: int) -> Dict[str, Any]:
        """Obtener anticipos pendientes de un chofer"""
        with self.uow:
            chofer = self.uow.choferes.get_by_id(chofer_id)
            if not chofer:
                raise EntityNotFoundException("Chofer", chofer_id)
            
            anticipos = self.uow.anticipos.get_pendientes_chofer(chofer_id)
            total = self.uow.anticipos.get_total_pendiente_chofer(chofer_id)
            
            return {
                "chofer": {"id": chofer.id, "nombre": f"{chofer.nombre} {chofer.apellido}"},
                "anticipos": [self._to_dict(a) for a in anticipos],
                "total_pendiente_bs": float(total)
            }
    
    def _to_dict(self, a, completo: bool = False) -> Dict[str, Any]:
        """Convertir entidad a diccionario"""
        return {
            "id": a.id,
            "chofer_id": a.chofer_id,
            "monto_bs": float(a.monto_bs),
            "fecha": str(a.fecha),
            "estado": a.estado,
            "motivo": a.motivo if hasattr(a, 'motivo') else None,
            "viaje_id": a.viaje_id if hasattr(a, 'viaje_id') else None
        }
