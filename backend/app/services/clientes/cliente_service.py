"""
Services - Clientes
"""
from typing import Optional, List, Dict, Any

from app.core.unit_of_work import UnitOfWork
from app.domain.exceptions import (
    EntityNotFoundException,
    DuplicateEntityException
)


class ClienteService:
    """Servicio de aplicación para gestión de clientes"""
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    def listar(
        self,
        page: int = 1,
        limit: int = 20,
        estado: Optional[str] = None,
        busqueda: Optional[str] = None
    ) -> Dict[str, Any]:
        """Listar clientes con filtros"""
        with self.uow:
            if busqueda:
                clientes = self.uow.clientes.get_by_nombre(busqueda)
                total = len(clientes)
            else:
                filtros = {"estado": estado} if estado else {}
                clientes = self.uow.clientes.get_all(
                    skip=(page - 1) * limit,
                    limit=limit,
                    filters=filtros
                )
                total = self.uow.clientes.count(filtros)
            
            return {
                "data": [self._to_dict(c) for c in clientes],
                "total": total,
                "page": page,
                "limit": limit
            }
    
    def obtener(self, cliente_id: int) -> Dict[str, Any]:
        """Obtener detalle de cliente"""
        with self.uow:
            cliente = self.uow.clientes.get_by_id(cliente_id)
            if not cliente:
                raise EntityNotFoundException("Cliente", cliente_id)
            
            # Contar viajes
            total_viajes = self.uow.clientes.contar_viajes(cliente_id)
            
            return {
                **self._to_dict(cliente, completo=True),
                "total_viajes": total_viajes
            }
    
    def crear(self, datos: Dict[str, Any], usuario_id: int) -> Dict[str, Any]:
        """Crear nuevo cliente"""
        with self.uow:
            # Validar NIT único
            if datos.get("nit") and self.uow.clientes.get_by_nit(datos["nit"]):
                raise DuplicateEntityException("Cliente", "nit", datos["nit"])
            
            cliente = self.uow.clientes.create({
                **datos,
                "estado": "ACTIVO"
            })
            self.uow.commit()
            
            return self._to_dict(cliente)
    
    def actualizar(self, cliente_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar cliente"""
        with self.uow:
            cliente = self.uow.clientes.get_by_id(cliente_id)
            if not cliente:
                raise EntityNotFoundException("Cliente", cliente_id)
            
            self.uow.clientes.update(cliente_id, datos)
            self.uow.commit()
            
            return self.obtener(cliente_id)
    
    def eliminar(self, cliente_id: int) -> bool:
        """Eliminar cliente (soft delete)"""
        with self.uow:
            cliente = self.uow.clientes.get_by_id(cliente_id)
            if not cliente:
                raise EntityNotFoundException("Cliente", cliente_id)
            
            self.uow.clientes.delete(cliente_id)
            self.uow.commit()
            return True
    
    def obtener_activos(self) -> List[Dict[str, Any]]:
        """Obtener clientes activos para selects"""
        with self.uow:
            clientes = self.uow.clientes.get_activos()
            return [{"id": c.id, "nombre": c.nombre} for c in clientes]
    
    def _to_dict(self, c, completo: bool = False) -> Dict[str, Any]:
        """Convertir entidad a diccionario"""
        data = {
            "id": c.id,
            "nombre": c.nombre,
            "nit": c.nit,
            "telefono": c.telefono,
            "estado": c.estado
        }
        if completo:
            data.update({
                "direccion": c.direccion,
                "email": c.email,
                "contacto": c.contacto,
                "notas": c.notas
            })
        return data
