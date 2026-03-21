"""
Repositorio para Liquidaciones
"""
from typing import Optional, List
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func, extract

from app.repositories.base_repository import BaseRepository
from app.models.liquidacion import Liquidacion


class LiquidacionRepository(BaseRepository[Liquidacion]):
    """Repositorio para gestión de liquidaciones"""
    
    def __init__(self, db: Session):
        super().__init__(db, Liquidacion)
    
    def get_with_viaje(self, liquidacion_id: int) -> Optional[Liquidacion]:
        """Obtener liquidación con datos del viaje"""
        return self.db.query(Liquidacion).options(
            joinedload(Liquidacion.viaje)
        ).filter(
            and_(
                Liquidacion.id == liquidacion_id,
                Liquidacion.deleted_at.is_(None)
            )
        ).first()
    
    def get_by_viaje(self, viaje_id: int) -> Optional[Liquidacion]:
        """Obtener liquidación de un viaje"""
        return self.db.query(Liquidacion).filter(
            and_(
                Liquidacion.viaje_id == viaje_id,
                Liquidacion.deleted_at.is_(None)
            )
        ).first()
    
    def get_by_periodo(
        self, 
        fecha_inicio: date, 
        fecha_fin: date
    ) -> List[Liquidacion]:
        """Obtener liquidaciones en un período"""
        return self.db.query(Liquidacion).filter(
            and_(
                Liquidacion.fecha >= fecha_inicio,
                Liquidacion.fecha <= fecha_fin,
                Liquidacion.deleted_at.is_(None)
            )
        ).order_by(Liquidacion.fecha.desc()).all()
    
    def get_totales_mes(self, año: int, mes: int) -> dict:
        """Obtener totales de liquidaciones del mes"""
        result = self.db.query(
            func.sum(Liquidacion.ingreso_bs).label("ingresos"),
            func.sum(Liquidacion.gastos_bs).label("gastos"),
            func.sum(Liquidacion.pago_socio_bs).label("pagos_socios"),
            func.count(Liquidacion.id).label("total")
        ).filter(
            and_(
                extract('year', Liquidacion.fecha) == año,
                extract('month', Liquidacion.fecha) == mes,
                Liquidacion.deleted_at.is_(None)
            )
        ).first()
        
        return {
            "ingresos_bs": result.ingresos or Decimal("0"),
            "gastos_bs": result.gastos or Decimal("0"),
            "pagos_socios_bs": result.pagos_socios or Decimal("0"),
            "total_liquidaciones": result.total or 0
        }
