"""
Repositorio para Mantenimientos
"""
from typing import Optional, List
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func

from app.infrastructure.repositories.base_repository import BaseRepository
from app.domain.entities.mantenimiento import Mantenimiento


class MantenimientoRepository(BaseRepository[Mantenimiento]):
    """Repositorio para gestión de mantenimientos"""
    
    def __init__(self, db: Session):
        super().__init__(db, Mantenimiento)
    
    def get_with_vehiculo(self, mant_id: int) -> Optional[Mantenimiento]:
        """Obtener mantenimiento con datos del vehículo"""
        return self.db.query(Mantenimiento).options(
            joinedload(Mantenimiento.vehiculo)
        ).filter(
            and_(
                Mantenimiento.id == mant_id,
                Mantenimiento.deleted_at.is_(None)
            )
        ).first()
    
    def get_by_vehiculo(self, vehiculo_id: int) -> List[Mantenimiento]:
        """Obtener mantenimientos de un vehículo"""
        return self.db.query(Mantenimiento).filter(
            and_(
                Mantenimiento.vehiculo_id == vehiculo_id,
                Mantenimiento.deleted_at.is_(None)
            )
        ).order_by(Mantenimiento.fecha.desc()).all()
    
    def get_pendientes(self) -> List[Mantenimiento]:
        """Obtener mantenimientos pendientes"""
        return self.db.query(Mantenimiento).filter(
            and_(
                Mantenimiento.estado == "PENDIENTE",
                Mantenimiento.deleted_at.is_(None)
            )
        ).all()
    
    def get_proximos(self, dias: int = 30) -> List[Mantenimiento]:
        """Obtener mantenimientos programados próximos"""
        from datetime import timedelta
        fecha_limite = date.today() + timedelta(days=dias)
        
        return self.db.query(Mantenimiento).filter(
            and_(
                Mantenimiento.fecha_programada <= fecha_limite,
                Mantenimiento.estado == "PROGRAMADO",
                Mantenimiento.deleted_at.is_(None)
            )
        ).order_by(Mantenimiento.fecha_programada).all()
    
    def get_costo_total_vehiculo(self, vehiculo_id: int) -> Decimal:
        """Obtener costo total de mantenimientos de un vehículo"""
        result = self.db.query(func.sum(Mantenimiento.costo_bs)).filter(
            and_(
                Mantenimiento.vehiculo_id == vehiculo_id,
                Mantenimiento.estado == "COMPLETADO",
                Mantenimiento.deleted_at.is_(None)
            )
        ).scalar()
        return result or Decimal("0")
