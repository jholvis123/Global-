"""
Services - Vehiculos
"""
from typing import Optional, List, Dict, Any
from datetime import date

from app.core.unit_of_work import UnitOfWork
from app.domain.exceptions import (
    EntityNotFoundException,
    BusinessRuleException,
    DuplicateEntityException
)


class VehiculoService:
    """Servicio de aplicación para gestión de vehículos"""
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    def listar(
        self,
        page: int = 1,
        limit: int = 20,
        estado: Optional[str] = None,
        socio_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Listar vehículos con filtros"""
        with self.uow:
            filtros = {}
            if estado:
                filtros["estado"] = estado
            if socio_id:
                filtros["socio_id"] = socio_id
            
            vehiculos = self.uow.vehiculos.get_all(
                skip=(page - 1) * limit,
                limit=limit,
                filters=filtros
            )
            total = self.uow.vehiculos.count(filtros)
            
            return {
                "data": [self._to_dict(v) for v in vehiculos],
                "total": total,
                "page": page,
                "limit": limit
            }
    
    def obtener(self, vehiculo_id: int) -> Dict[str, Any]:
        """Obtener detalle de vehículo"""
        with self.uow:
            vehiculo = self.uow.vehiculos.get_with_socio(vehiculo_id)
            if not vehiculo:
                raise EntityNotFoundException("Vehículo", vehiculo_id)
            return self._to_dict(vehiculo, incluir_socio=True)
    
    def crear(self, datos: Dict[str, Any], usuario_id: int) -> Dict[str, Any]:
        """Crear nuevo vehículo"""
        with self.uow:
            # Validar placa única
            if self.uow.vehiculos.get_by_placa(datos["placa"]):
                raise DuplicateEntityException("Vehículo", "placa", datos["placa"])
            
            # Validar socio existe
            socio = self.uow.socios.get_by_id(datos["socio_id"])
            if not socio:
                raise EntityNotFoundException("Socio", datos["socio_id"])
            
            vehiculo = self.uow.vehiculos.create({
                **datos,
                "placa": datos["placa"].upper(),
                "estado": "DISPONIBLE"
            })
            self.uow.commit()
            
            return self._to_dict(vehiculo)
    
    def actualizar(self, vehiculo_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar vehículo"""
        with self.uow:
            vehiculo = self.uow.vehiculos.get_by_id(vehiculo_id)
            if not vehiculo:
                raise EntityNotFoundException("Vehículo", vehiculo_id)
            
            # Validar placa única si cambió
            if "placa" in datos and datos["placa"] != vehiculo.placa:
                existente = self.uow.vehiculos.get_by_placa(datos["placa"])
                if existente:
                    raise DuplicateEntityException("Vehículo", "placa", datos["placa"])
            
            self.uow.vehiculos.update(vehiculo_id, datos)
            self.uow.commit()
            
            return self.obtener(vehiculo_id)
    
    def eliminar(self, vehiculo_id: int) -> bool:
        """Eliminar vehículo (soft delete)"""
        with self.uow:
            vehiculo = self.uow.vehiculos.get_by_id(vehiculo_id)
            if not vehiculo:
                raise EntityNotFoundException("Vehículo", vehiculo_id)
            
            if vehiculo.estado == "EN_VIAJE":
                raise BusinessRuleException("No se puede eliminar un vehículo en viaje")
            
            self.uow.vehiculos.delete(vehiculo_id)
            self.uow.commit()
            return True
    
    def obtener_disponibles(self) -> List[Dict[str, Any]]:
        """Obtener vehículos disponibles para asignar"""
        with self.uow:
            vehiculos = self.uow.vehiculos.get_disponibles()
            return [self._to_dict(v) for v in vehiculos]
    
    def _to_dict(self, v, incluir_socio: bool = False) -> Dict[str, Any]:
        """Convertir entidad a diccionario"""
        data = {
            "id": v.id,
            "placa": v.placa,
            "marca": v.marca,
            "modelo": v.modelo,
            "año": v.año,
            "tipo": v.tipo,
            "capacidad_ton": float(v.capacidad_ton) if v.capacidad_ton else None,
            "estado": v.estado
        }
        if incluir_socio and v.socio:
            data["socio"] = {
                "id": v.socio.id,
                "nombre": f"{v.socio.nombre} {v.socio.apellido}"
            }
        return data
