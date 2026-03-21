"""
Repositorio para Choferes
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.repositories.base_repository import BaseRepository
from app.models.chofer import Chofer


class ChoferRepository(BaseRepository[Chofer]):
    """Repositorio para gestión de choferes"""
    
    def __init__(self, db: Session):
        super().__init__(db, Chofer)
    
    def get_disponibles(self) -> List[Chofer]:
        """Obtener choferes disponibles"""
        return self.db.query(Chofer).filter(
            and_(
                Chofer.estado == "DISPONIBLE",
                Chofer.deleted_at.is_(None)
            )
        ).all()
    
    def get_by_ci(self, ci: str) -> Optional[Chofer]:
        """Buscar chofer por CI"""
        return self.db.query(Chofer).filter(
            and_(
                Chofer.ci == ci,
                Chofer.deleted_at.is_(None)
            )
        ).first()
    
    def get_by_licencia(self, licencia: str) -> Optional[Chofer]:
        """Buscar chofer por número de licencia"""
        return self.db.query(Chofer).filter(
            and_(
                Chofer.nro_licencia == licencia,
                Chofer.deleted_at.is_(None)
            )
        ).first()
    
    def actualizar_estado(self, chofer_id: int, estado: str) -> bool:
        """Actualizar estado del chofer"""
        return self.update(chofer_id, {"estado": estado}) is not None
    
    def get_con_licencia_vencida(self) -> List[Chofer]:
        """Obtener choferes con licencia vencida"""
        from datetime import date
        return self.db.query(Chofer).filter(
            and_(
                Chofer.deleted_at.is_(None),
                Chofer.fecha_venc_licencia < date.today()
            )
        ).all()
    
    def get_activos(self) -> List[Chofer]:
        """Obtener todos los choferes activos"""
        return self.db.query(Chofer).filter(
            and_(
                Chofer.estado.in_(["DISPONIBLE", "EN_VIAJE"]),
                Chofer.deleted_at.is_(None)
            )
        ).all()
