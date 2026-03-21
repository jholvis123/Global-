"""
Services - Mantenimientos
"""
from typing import Optional, List, Dict, Any
from datetime import date
from decimal import Decimal

from app.core.unit_of_work import UnitOfWork
from app.domain.exceptions import (
    EntityNotFoundException,
    BusinessRuleException
)


class MantenimientoService:
    """Servicio de aplicación para gestión de mantenimientos"""
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    def listar(
        self,
        page: int = 1,
        limit: int = 20,
        vehiculo_id: Optional[int] = None,
        estado: Optional[str] = None,
        tipo: Optional[str] = None
    ) -> Dict[str, Any]:
        """Listar mantenimientos con filtros"""
        with self.uow:
            filtros = {}
            if vehiculo_id:
                filtros["vehiculo_id"] = vehiculo_id
            if estado:
                filtros["estado"] = estado
            if tipo:
                filtros["tipo"] = tipo
            
            mantenimientos = self.uow.mantenimientos.get_all(
                skip=(page - 1) * limit,
                limit=limit,
                filters=filtros
            )
            total = self.uow.mantenimientos.count(filtros)
            
            return {
                "data": [self._to_dict(m) for m in mantenimientos],
                "total": total,
                "page": page,
                "limit": limit
            }
    
    def obtener(self, mant_id: int) -> Dict[str, Any]:
        """Obtener detalle de mantenimiento"""
        with self.uow:
            mant = self.uow.mantenimientos.get_with_vehiculo(mant_id)
            if not mant:
                raise EntityNotFoundException("Mantenimiento", mant_id)
            return self._to_dict(mant, completo=True)
    
    def crear(self, datos: Dict[str, Any], usuario_id: int) -> Dict[str, Any]:
        """Crear nuevo mantenimiento"""
        with self.uow:
            # Validar vehículo existe
            vehiculo = self.uow.vehiculos.get_by_id(datos["vehiculo_id"])
            if not vehiculo:
                raise EntityNotFoundException("Vehículo", datos["vehiculo_id"])
            
            mant = self.uow.mantenimientos.create({
                **datos,
                "estado": datos.get("estado", "PROGRAMADO"),
                "creado_por": usuario_id
            })
            
            # Si es mantenimiento inmediato, cambiar estado del vehículo
            if datos.get("estado") == "EN_PROCESO":
                self.uow.vehiculos.actualizar_estado(vehiculo.id, "MANTENIMIENTO")
            
            self.uow.commit()
            return self._to_dict(mant)
    
    def actualizar(self, mant_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar mantenimiento"""
        with self.uow:
            mant = self.uow.mantenimientos.get_by_id(mant_id)
            if not mant:
                raise EntityNotFoundException("Mantenimiento", mant_id)
            
            self.uow.mantenimientos.update(mant_id, datos)
            self.uow.commit()
            
            return self.obtener(mant_id)
    
    def completar(self, mant_id: int, costo_bs: float, notas: str = None) -> Dict[str, Any]:
        """Marcar mantenimiento como completado"""
        with self.uow:
            mant = self.uow.mantenimientos.get_with_vehiculo(mant_id)
            if not mant:
                raise EntityNotFoundException("Mantenimiento", mant_id)
            
            if mant.estado == "COMPLETADO":
                raise BusinessRuleException("El mantenimiento ya está completado")
            
            self.uow.mantenimientos.update(mant_id, {
                "estado": "COMPLETADO",
                "costo_bs": Decimal(str(costo_bs)),
                "fecha_completado": date.today(),
                "notas": notas
            })
            
            # Liberar vehículo
            self.uow.vehiculos.actualizar_estado(mant.vehiculo_id, "DISPONIBLE")
            
            self.uow.commit()
            return self.obtener(mant_id)
    
    def obtener_proximos(self, dias: int = 30) -> List[Dict[str, Any]]:
        """Obtener mantenimientos programados próximos"""
        with self.uow:
            mantenimientos = self.uow.mantenimientos.get_proximos(dias)
            return [self._to_dict(m) for m in mantenimientos]
    
    def obtener_historial_vehiculo(self, vehiculo_id: int) -> Dict[str, Any]:
        """Obtener historial de mantenimientos de un vehículo"""
        with self.uow:
            vehiculo = self.uow.vehiculos.get_by_id(vehiculo_id)
            if not vehiculo:
                raise EntityNotFoundException("Vehículo", vehiculo_id)
            
            mantenimientos = self.uow.mantenimientos.get_by_vehiculo(vehiculo_id)
            costo_total = self.uow.mantenimientos.get_costo_total_vehiculo(vehiculo_id)
            
            return {
                "vehiculo": {"id": vehiculo.id, "placa": vehiculo.placa},
                "mantenimientos": [self._to_dict(m) for m in mantenimientos],
                "costo_total_bs": float(costo_total),
                "total_mantenimientos": len(mantenimientos)
            }
    
    def _to_dict(self, m, completo: bool = False) -> Dict[str, Any]:
        """Convertir entidad a diccionario"""
        data = {
            "id": m.id,
            "vehiculo_id": m.vehiculo_id,
            "tipo": m.tipo,
            "descripcion": m.descripcion,
            "estado": m.estado,
            "costo_bs": float(m.costo_bs) if m.costo_bs else None,
            "fecha": str(m.fecha) if hasattr(m, 'fecha') else None
        }
        if completo and hasattr(m, 'vehiculo') and m.vehiculo:
            data["vehiculo"] = {
                "placa": m.vehiculo.placa,
                "marca": m.vehiculo.marca,
                "modelo": m.vehiculo.modelo
            }
        return data
