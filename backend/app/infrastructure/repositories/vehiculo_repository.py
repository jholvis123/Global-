"""
Repositorio para Vehículos
"""
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc

from app.infrastructure.repositories.base_repository import BaseRepository
from app.domain.entities.vehiculo import Vehiculo


class VehiculoRepository(BaseRepository[Vehiculo]):
    """Repositorio para gestión de vehículos"""
    
    def __init__(self, db: Session):
        super().__init__(db, Vehiculo)
    
    def get_with_socio(self, vehiculo_id: int) -> Optional[Vehiculo]:
        """Obtener vehículo con datos del socio"""
        return self.db.query(Vehiculo).options(
            joinedload(Vehiculo.socio)
        ).filter(
            and_(
                Vehiculo.id == vehiculo_id,
                Vehiculo.deleted_at.is_(None)
            )
        ).first()
    
    def get_disponibles(self) -> List[Vehiculo]:
        """Obtener vehículos disponibles para viaje"""
        return self.db.query(Vehiculo).filter(
            and_(
                Vehiculo.estado == "DISPONIBLE",
                Vehiculo.deleted_at.is_(None)
            )
        ).all()
    
    def get_by_socio(self, socio_id: int) -> List[Vehiculo]:
        """Obtener vehículos de un socio"""
        return self.db.query(Vehiculo).filter(
            and_(
                Vehiculo.socio_id == socio_id,
                Vehiculo.deleted_at.is_(None)
            )
        ).all()
    
    def get_by_placa(self, placa: str) -> Optional[Vehiculo]:
        """Buscar vehículo por placa"""
        return self.db.query(Vehiculo).filter(
            and_(
                Vehiculo.placa == placa.upper(),
                Vehiculo.deleted_at.is_(None)
            )
        ).first()
    
    def get_en_mantenimiento(self) -> List[Vehiculo]:
        """Obtener vehículos en mantenimiento"""
        return self.db.query(Vehiculo).filter(
            and_(
                Vehiculo.estado == "MANTENIMIENTO",
                Vehiculo.deleted_at.is_(None)
            )
        ).all()
    
    def actualizar_estado(self, vehiculo_id: int, estado: str) -> bool:
        """Actualizar estado del vehículo"""
        return self.update(vehiculo_id, {"estado": estado}) is not None
    
    def get_con_documentos_vencidos(self, fecha_limite: date) -> List[Vehiculo]:
        """Obtener vehículos con documentos próximos a vencer"""
        return self.db.query(Vehiculo).filter(
            and_(
                Vehiculo.deleted_at.is_(None),
                Vehiculo.fecha_venc_soat <= fecha_limite
            )
        ).all()
