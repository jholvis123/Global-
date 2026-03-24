"""
Repositorio para Clientes
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.infrastructure.repositories.base_repository import BaseRepository
from app.domain.entities.cliente import Cliente


class ClienteRepository(BaseRepository[Cliente]):
    """Repositorio para gestión de clientes"""
    
    def __init__(self, db: Session):
        super().__init__(db, Cliente)
    
    def get_activos(self) -> List[Cliente]:
        """Obtener clientes activos"""
        return self.db.query(Cliente).filter(
            and_(
                Cliente.estado == "ACTIVO",
                Cliente.deleted_at.is_(None)
            )
        ).all()
    
    def get_by_nit(self, nit: str) -> Optional[Cliente]:
        """Buscar cliente por NIT"""
        return self.db.query(Cliente).filter(
            and_(
                Cliente.nit == nit,
                Cliente.deleted_at.is_(None)
            )
        ).first()
    
    def get_by_nombre(self, nombre: str) -> List[Cliente]:
        """Buscar clientes por nombre (parcial)"""
        return self.db.query(Cliente).filter(
            and_(
                Cliente.nombre.ilike(f"%{nombre}%"),
                Cliente.deleted_at.is_(None)
            )
        ).all()
    
    def get_con_viajes_activos(self) -> List[Cliente]:
        """Obtener clientes con viajes activos"""
        from app.domain.entities.viaje import Viaje
        return self.db.query(Cliente).join(Viaje).filter(
            and_(
                Viaje.estado.in_(["PLANIFICADO", "EN_RUTA"]),
                Viaje.deleted_at.is_(None),
                Cliente.deleted_at.is_(None)
            )
        ).distinct().all()
    
    def contar_viajes(self, cliente_id: int) -> int:
        """Contar viajes de un cliente"""
        from app.domain.entities.viaje import Viaje
        return self.db.query(func.count(Viaje.id)).filter(
            and_(
                Viaje.cliente_id == cliente_id,
                Viaje.deleted_at.is_(None)
            )
        ).scalar()
