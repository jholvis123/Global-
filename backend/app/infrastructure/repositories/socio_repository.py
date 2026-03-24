from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func, desc
from decimal import Decimal
from app.domain.entities import Socio, Vehiculo, Viaje, Anticipo, Liquidacion
from app.infrastructure.repositories.base_repository import BaseRepository
from datetime import date, datetime


class SocioRepository(BaseRepository[Socio]):
    """Repositorio para gestión de socios"""
    
    def __init__(self, db: Session):
        super().__init__(db, Socio)
    
    def get_by_nit(self, nit: str) -> Optional[Socio]:
        """Obtener socio por NIT"""
        return self.get_by_field('nit', nit)
    
    def get_by_ci(self, ci: str) -> Optional[Socio]:
        """Obtener socio por CI"""
        return self.get_by_field('ci', ci)
    
    def get_with_vehiculos(self, socio_id: int) -> Optional[Socio]:
        """Obtener socio con sus vehículos"""
        return self.db.query(Socio).options(
            joinedload(Socio.vehiculos)
        ).filter(
            and_(
                Socio.id == socio_id,
                Socio.deleted_at.is_(None)
            )
        ).first()
    
    def get_active_socios(self) -> List[Socio]:
        """Obtener socios activos"""
        return self.db.query(Socio).filter(
            and_(
                Socio.estado == "ACTIVO",
                Socio.deleted_at.is_(None)
            )
        ).all()
    
    def update_saldo_anticipos(self, socio_id: int, monto: Decimal, operacion: str) -> bool:
        """Actualizar saldo de anticipos del socio"""
        socio = self.get_by_id(socio_id)
        if not socio:
            return False
        
        if operacion == "AGREGAR":
            socio.saldo_anticipos += monto
        elif operacion == "RESTAR":
            socio.saldo_anticipos -= monto
        elif operacion == "SET":
            socio.saldo_anticipos = monto
        
        self.db.commit()
        return True
    
    def get_socios_con_saldo_pendiente(self) -> List[Socio]:
        """Obtener socios con saldo de anticipos pendiente"""
        return self.db.query(Socio).filter(
            and_(
                Socio.saldo_anticipos != 0,
                Socio.deleted_at.is_(None)
            )
        ).all()
    
    def get_reporte_socio(
        self, 
        socio_id: int, 
        fecha_inicio: date = None, 
        fecha_fin: date = None
    ) -> Dict[str, Any]:
        """Obtener reporte completo de un socio"""
        socio = self.get_by_id(socio_id)
        if not socio:
            return {}
        
        # Query base para viajes del socio
        query_viajes = self.db.query(Viaje).join(Vehiculo).filter(
            and_(
                Vehiculo.socio_id == socio_id,
                Viaje.deleted_at.is_(None)
            )
        )
        
        # Aplicar filtros de fecha si se proporcionan
        if fecha_inicio:
            query_viajes = query_viajes.filter(Viaje.fecha_salida >= fecha_inicio)
        if fecha_fin:
            query_viajes = query_viajes.filter(Viaje.fecha_salida <= fecha_fin)
        
        viajes = query_viajes.all()
        
        # Calcular estadísticas
        total_viajes = len(viajes)
        ingresos_generados = sum(viaje.ingreso_total_bs for viaje in viajes)
        
        # Anticipos en el período
        query_anticipos = self.db.query(Anticipo).filter(
            and_(
                Anticipo.socio_id == socio_id,
                Anticipo.deleted_at.is_(None)
            )
        )
        
        if fecha_inicio:
            query_anticipos = query_anticipos.filter(Anticipo.fecha >= fecha_inicio)
        if fecha_fin:
            query_anticipos = query_anticipos.filter(Anticipo.fecha <= fecha_fin)
        
        anticipos = query_anticipos.all()
        anticipos_recibidos = sum(anticipo.monto_bs for anticipo in anticipos)
        
        # Liquidaciones en el período
        liquidaciones_ids = [viaje.id for viaje in viajes]
        liquidaciones = []
        pago_total_recibido = Decimal('0.00')
        
        if liquidaciones_ids:
            liquidaciones = self.db.query(Liquidacion).filter(
                Liquidacion.viaje_id.in_(liquidaciones_ids)
            ).all()
            pago_total_recibido = sum(liq.pago_socio_bs for liq in liquidaciones)
        
        # Vehículos del socio
        vehiculos = self.db.query(Vehiculo).filter(
            and_(
                Vehiculo.socio_id == socio_id,
                Vehiculo.deleted_at.is_(None)
            )
        ).all()
        
        return {
            "socio": socio,
            "periodo_inicio": fecha_inicio,
            "periodo_fin": fecha_fin,
            "vehiculos_cantidad": len(vehiculos),
            "vehiculos_activos": len([v for v in vehiculos if v.estado == "ACTIVO"]),
            "total_viajes": total_viajes,
            "ingresos_generados": ingresos_generados,
            "anticipos_recibidos": anticipos_recibidos,
            "pago_total_recibido": pago_total_recibido,
            "saldo_actual": socio.saldo_anticipos,
            "vehiculos": vehiculos,
            "viajes_recientes": viajes[-10:] if viajes else [],
            "liquidaciones": liquidaciones
        }
    
    def get_ranking_socios_productivos(self, fecha_inicio: date = None, fecha_fin: date = None, limit: int = 10) -> List[Dict]:
        """Obtener ranking de socios más productivos"""
        # Subquery para calcular estadísticas por socio
        subquery = self.db.query(
            Socio.id.label('socio_id'),
            Socio.nombre.label('socio_nombre'),
            func.count(Viaje.id).label('total_viajes'),
            func.sum(Viaje.ingreso_total_bs).label('ingresos_total')
        ).join(Vehiculo, Socio.id == Vehiculo.socio_id)\
        .join(Viaje, Vehiculo.id == Viaje.vehiculo_id)\
        .filter(
            and_(
                Socio.deleted_at.is_(None),
                Viaje.deleted_at.is_(None),
                Viaje.estado == "LIQUIDADO"
            )
        )
        
        # Aplicar filtros de fecha
        if fecha_inicio:
            subquery = subquery.filter(Viaje.fecha_salida >= fecha_inicio)
        if fecha_fin:
            subquery = subquery.filter(Viaje.fecha_salida <= fecha_fin)
        
        # Agrupar y ordenar
        result = subquery.group_by(Socio.id, Socio.nombre)\
                        .order_by(desc('ingresos_total'))\
                        .limit(limit).all()
        
        return [
            {
                "socio_id": r.socio_id,
                "socio_nombre": r.socio_nombre,
                "total_viajes": r.total_viajes or 0,
                "ingresos_total": float(r.ingresos_total or 0)
            }
            for r in result
        ]
    
    def search_socios(self, search_term: str) -> List[Socio]:
        """Buscar socios por nombre, NIT o CI"""
        return self.search(search_term, ['nombre', 'nit', 'ci'])
    
    def get_socios_por_estado(self, estado: str) -> List[Socio]:
        """Obtener socios por estado"""
        return self.db.query(Socio).filter(
            and_(
                Socio.estado == estado,
                Socio.deleted_at.is_(None)
            )
        ).all()
    
    def get_estadisticas_generales(self) -> Dict[str, Any]:
        """Obtener estadísticas generales de socios"""
        total_socios = self.db.query(Socio).filter(Socio.deleted_at.is_(None)).count()
        socios_activos = self.db.query(Socio).filter(
            and_(Socio.estado == "ACTIVO", Socio.deleted_at.is_(None))
        ).count()
        
        # Socios con saldo pendiente
        socios_con_saldo = self.db.query(Socio).filter(
            and_(
                Socio.saldo_anticipos != 0,
                Socio.deleted_at.is_(None)
            )
        ).count()
        
        # Suma total de anticipos pendientes
        saldo_total = self.db.query(func.sum(Socio.saldo_anticipos)).filter(
            Socio.deleted_at.is_(None)
        ).scalar() or Decimal('0.00')
        
        return {
            "total_socios": total_socios,
            "socios_activos": socios_activos,
            "socios_inactivos": total_socios - socios_activos,
            "socios_con_saldo_pendiente": socios_con_saldo,
            "saldo_total_anticipos": float(saldo_total)
        }