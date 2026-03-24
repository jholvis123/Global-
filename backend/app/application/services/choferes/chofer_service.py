"""
Services - Choferes
"""
from typing import Optional, List, Dict, Any
from datetime import date

from app.core.unit_of_work import UnitOfWork
from app.domain.exceptions import (
    EntityNotFoundException,
    BusinessRuleException,
    DuplicateEntityException
)


class ChoferService:
    """Servicio de aplicación para gestión de choferes"""
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    def listar(
        self,
        page: int = 1,
        limit: int = 20,
        estado: Optional[str] = None,
        busqueda: Optional[str] = None
    ) -> Dict[str, Any]:
        """Listar choferes con filtros"""
        with self.uow:
            filtros = {}
            if estado:
                filtros["estado"] = estado
            
            if busqueda:
                choferes = self.uow.choferes.search(
                    busqueda, 
                    ["nombre", "apellido", "ci"]
                )
                total = len(choferes)
            else:
                choferes = self.uow.choferes.get_all(
                    skip=(page - 1) * limit,
                    limit=limit,
                    filters=filtros
                )
                total = self.uow.choferes.count(filtros)
            
            return {
                "data": [self._to_dict(c) for c in choferes],
                "total": total,
                "page": page,
                "limit": limit
            }
    
    def obtener(self, chofer_id: int) -> Dict[str, Any]:
        """Obtener detalle de chofer"""
        with self.uow:
            chofer = self.uow.choferes.get_by_id(chofer_id)
            if not chofer:
                raise EntityNotFoundException("Chofer", chofer_id)
            return self._to_dict(chofer, completo=True)
    
    def crear(self, datos: Dict[str, Any], usuario_id: int) -> Dict[str, Any]:
        """Crear nuevo chofer"""
        with self.uow:
            # Validar CI único
            if self.uow.choferes.get_by_ci(datos["ci"]):
                raise DuplicateEntityException("Chofer", "ci", datos["ci"])
            
            # Validar licencia única
            if self.uow.choferes.get_by_licencia(datos.get("nro_licencia", "")):
                raise DuplicateEntityException("Chofer", "licencia", datos["nro_licencia"])
            
            chofer = self.uow.choferes.create({
                **datos,
                "estado": "DISPONIBLE"
            })
            self.uow.commit()
            
            return self._to_dict(chofer)
    
    def actualizar(self, chofer_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar chofer"""
        with self.uow:
            chofer = self.uow.choferes.get_by_id(chofer_id)
            if not chofer:
                raise EntityNotFoundException("Chofer", chofer_id)
            
            self.uow.choferes.update(chofer_id, datos)
            self.uow.commit()
            
            return self.obtener(chofer_id)
    
    def eliminar(self, chofer_id: int) -> bool:
        """Eliminar chofer (soft delete)"""
        with self.uow:
            chofer = self.uow.choferes.get_by_id(chofer_id)
            if not chofer:
                raise EntityNotFoundException("Chofer", chofer_id)
            
            if chofer.estado == "EN_VIAJE":
                raise BusinessRuleException("No se puede eliminar un chofer en viaje")
            
            self.uow.choferes.delete(chofer_id)
            self.uow.commit()
            return True
    
    def obtener_disponibles(self) -> List[Dict[str, Any]]:
        """Obtener choferes disponibles"""
        with self.uow:
            choferes = self.uow.choferes.get_disponibles()
            return [self._to_dict(c) for c in choferes]
    
    def _to_dict(self, c, completo: bool = False) -> Dict[str, Any]:
        """Convertir entidad a diccionario"""
        data = {
            "id": c.id,
            "nombre": c.nombre,
            "apellido": c.apellido,
            "nombre_completo": f"{c.nombre} {c.apellido}",
            "ci": c.ci,
            "telefono": c.telefono,
            "estado": c.estado
        }
        if completo:
            data.update({
                "direccion": c.direccion,
                "nro_licencia": c.nro_licencia,
                "categoria_licencia": c.categoria_licencia,
                "fecha_venc_licencia": str(c.fecha_venc_licencia) if c.fecha_venc_licencia else None,
                "fecha_nacimiento": str(c.fecha_nacimiento) if c.fecha_nacimiento else None
            })
        return data
