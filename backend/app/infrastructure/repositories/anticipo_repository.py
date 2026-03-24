"""
Repositorio para Anticipos
"""
from typing import Optional, List
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func

from app.infrastructure.repositories.base_repository import BaseRepository
from app.domain.entities.anticipo import Anticipo


class AnticipoRepository(BaseRepository[Anticipo]):
    """Repositorio para gestión de anticipos"""
    
    def __init__(self, db: Session):
        super().__init__(db, Anticipo)
    
    def get_by_chofer(self, chofer_id: int) -> List[Anticipo]:
        """Obtener anticipos de un chofer"""
        return self.db.query(Anticipo).filter(
            and_(
                Anticipo.chofer_id == chofer_id,
                Anticipo.deleted_at.is_(None)
            )
        ).order_by(Anticipo.fecha.desc()).all()
    
    def get_pendientes_chofer(self, chofer_id: int) -> List[Anticipo]:
        """Obtener anticipos pendientes de un chofer"""
        return self.db.query(Anticipo).filter(
            and_(
                Anticipo.chofer_id == chofer_id,
                Anticipo.estado == "PENDIENTE",
                Anticipo.deleted_at.is_(None)
            )
        ).all()
    
    def get_total_pendiente_chofer(self, chofer_id: int) -> Decimal:
        """Obtener total de anticipos pendientes de un chofer"""
        result = self.db.query(func.sum(Anticipo.monto_bs)).filter(
            and_(
                Anticipo.chofer_id == chofer_id,
                Anticipo.estado == "PENDIENTE",
                Anticipo.deleted_at.is_(None)
            )
        ).scalar()
        return result or Decimal("0")
    
    def marcar_descontado(self, anticipo_id: int, viaje_id: int) -> bool:
        """Marcar anticipo como descontado"""
        return self.update(anticipo_id, {
            "estado": "DESCONTADO",
            "viaje_id": viaje_id
        }) is not None
    
    def get_by_periodo(
        self, 
        fecha_inicio: date, 
        fecha_fin: date
    ) -> List[Anticipo]:
        """Obtener anticipos en un período"""
        return self.db.query(Anticipo).filter(
            and_(
                Anticipo.fecha >= fecha_inicio,
                Anticipo.fecha <= fecha_fin,
                Anticipo.deleted_at.is_(None)
            )
        ).order_by(Anticipo.fecha.desc()).all()
