from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func, desc, asc, extract, text
from decimal import Decimal
from datetime import date, datetime
from app.models import Viaje, GastoViaje, Vehiculo, Chofer, Cliente, Socio, Liquidacion
from app.repositories.base_repository import BaseRepository


class ViajeRepository(BaseRepository[Viaje]):
    """Repositorio para gestión de viajes"""
    
    def __init__(self, db: Session):
        super().__init__(db, Viaje)
    
    def get_with_relations(self, viaje_id: int) -> Optional[Viaje]:
        """Obtener viaje con todas las relaciones cargadas"""
        return self.db.query(Viaje).options(
            joinedload(Viaje.cliente),
            joinedload(Viaje.vehiculo).joinedload(Vehiculo.socio),
            joinedload(Viaje.chofer),
            joinedload(Viaje.gastos),
            joinedload(Viaje.liquidacion)
        ).filter(
            and_(
                Viaje.id == viaje_id,
                Viaje.deleted_at.is_(None)
            )
        ).first()
    
    def get_by_estado(self, estado: str) -> List[Viaje]:
        """Obtener viajes por estado"""
        return self.db.query(Viaje).filter(
            and_(
                Viaje.estado == estado,
                Viaje.deleted_at.is_(None)
            )
        ).all()
    
    def get_viajes_pendientes_liquidacion(self) -> List[Viaje]:
        """Obtener viajes entregados pendientes de liquidación"""
        return self.db.query(Viaje).filter(
            and_(
                Viaje.estado == "ENTREGADO",
                Viaje.deleted_at.is_(None)
            )
        ).all()
    
    def get_by_chofer(self, chofer_id: int, fecha_inicio: date = None, fecha_fin: date = None) -> List[Viaje]:
        """Obtener viajes de un chofer en un período"""
        query = self.db.query(Viaje).filter(
            and_(
                Viaje.chofer_id == chofer_id,
                Viaje.deleted_at.is_(None)
            )
        )
        
        if fecha_inicio:
            query = query.filter(Viaje.fecha_salida >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Viaje.fecha_salida <= fecha_fin)
        
        return query.order_by(desc(Viaje.fecha_salida)).all()
    
    def get_by_vehiculo(self, vehiculo_id: int, fecha_inicio: date = None, fecha_fin: date = None) -> List[Viaje]:
        """Obtener viajes de un vehículo en un período"""
        query = self.db.query(Viaje).filter(
            and_(
                Viaje.vehiculo_id == vehiculo_id,
                Viaje.deleted_at.is_(None)
            )
        )
        
        if fecha_inicio:
            query = query.filter(Viaje.fecha_salida >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Viaje.fecha_salida <= fecha_fin)
        
        return query.order_by(desc(Viaje.fecha_salida)).all()
    
    def get_by_socio(self, socio_id: int, fecha_inicio: date = None, fecha_fin: date = None) -> List[Viaje]:
        """Obtener viajes de vehículos de un socio"""
        query = self.db.query(Viaje).join(Vehiculo).filter(
            and_(
                Vehiculo.socio_id == socio_id,
                Viaje.deleted_at.is_(None)
            )
        )
        
        if fecha_inicio:
            query = query.filter(Viaje.fecha_salida >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Viaje.fecha_salida <= fecha_fin)
        
        return query.order_by(desc(Viaje.fecha_salida)).all()
    
    def get_by_cliente(self, cliente_id: int, fecha_inicio: date = None, fecha_fin: date = None) -> List[Viaje]:
        """Obtener viajes de un cliente"""
        query = self.db.query(Viaje).filter(
            and_(
                Viaje.cliente_id == cliente_id,
                Viaje.deleted_at.is_(None)
            )
        )
        
        if fecha_inicio:
            query = query.filter(Viaje.fecha_salida >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Viaje.fecha_salida <= fecha_fin)
        
        return query.order_by(desc(Viaje.fecha_salida)).all()
    
    def get_by_tipo_carga(self, tipo_carga: str, fecha_inicio: date = None, fecha_fin: date = None) -> List[Viaje]:
        """Obtener viajes por tipo de carga"""
        query = self.db.query(Viaje).filter(
            and_(
                Viaje.tipo_carga == tipo_carga,
                Viaje.deleted_at.is_(None)
            )
        )
        
        if fecha_inicio:
            query = query.filter(Viaje.fecha_salida >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Viaje.fecha_salida <= fecha_fin)
        
        return query.all()
    
    def get_viajes_fecha(self, fecha: date) -> List[Viaje]:
        """Obtener viajes de una fecha específica"""
        return self.db.query(Viaje).filter(
            and_(
                func.date(Viaje.fecha_salida) == fecha,
                Viaje.deleted_at.is_(None)
            )
        ).all()
    
    def get_estadisticas_diarias(self, fecha: date) -> Dict[str, Any]:
        """Obtener estadísticas de viajes para un día"""
        viajes = self.get_viajes_fecha(fecha)
        
        total_viajes = len(viajes)
        ingresos_total = sum(viaje.ingreso_total_bs for viaje in viajes)
        gastos_total = sum(viaje.total_gastos_bs for viaje in viajes)
        
        # Contar por estado
        estados = {}
        for viaje in viajes:
            estados[viaje.estado] = estados.get(viaje.estado, 0) + 1
        
        # Contar por tipo de carga
        tipos_carga = {}
        for viaje in viajes:
            tipos_carga[viaje.tipo_carga] = tipos_carga.get(viaje.tipo_carga, 0) + 1
        
        return {
            "fecha": fecha,
            "total_viajes": total_viajes,
            "ingresos_bs": ingresos_total,
            "gastos_bs": gastos_total,
            "ganancia_bs": ingresos_total - gastos_total,
            "por_estado": estados,
            "por_tipo_carga": tipos_carga
        }
    
    def get_estadisticas_mensuales(self, año: int, mes: int) -> Dict[str, Any]:
        """Obtener estadísticas de viajes para un mes"""
        viajes = self.db.query(Viaje).filter(
            and_(
                extract('year', Viaje.fecha_salida) == año,
                extract('month', Viaje.fecha_salida) == mes,
                Viaje.deleted_at.is_(None)
            )
        ).all()
        
        total_viajes = len(viajes)
        ingresos_total = sum(viaje.ingreso_total_bs for viaje in viajes)
        gastos_total = sum(viaje.total_gastos_bs for viaje in viajes)
        
        return {
            "año": año,
            "mes": mes,
            "total_viajes": total_viajes,
            "ingresos_bs": ingresos_total,
            "gastos_bs": gastos_total,
            "ganancia_bs": ingresos_total - gastos_total
        }
    
    def get_reporte_por_tipo_carga(
        self, 
        fecha_inicio: date = None, 
        fecha_fin: date = None
    ) -> List[Dict[str, Any]]:
        """Obtener reporte agrupado por tipo de carga"""
        query = self.db.query(
            Viaje.tipo_carga,
            func.count(Viaje.id).label('total_viajes'),
            func.sum(Viaje.peso_ton).label('peso_total_ton'),
            func.sum(
                text("""
                CASE 
                    WHEN tarifa_tipo = 'TON' THEN peso_ton * tarifa_valor
                    WHEN tarifa_tipo = 'KM' THEN ISNULL(km_real, km_estimado) * tarifa_valor
                    WHEN tarifa_tipo = 'FIJA' THEN tarifa_valor
                END
                """)
            ).label('ingreso_total_bs')
        ).filter(Viaje.deleted_at.is_(None))
        
        if fecha_inicio:
            query = query.filter(Viaje.fecha_salida >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Viaje.fecha_salida <= fecha_fin)
        
        result = query.group_by(Viaje.tipo_carga).all()
        
        # Obtener gastos por tipo de carga
        gastos_subquery = self.db.query(
            Viaje.tipo_carga,
            func.sum(GastoViaje.monto_bs).label('gasto_total_bs')
        ).join(GastoViaje, Viaje.id == GastoViaje.viaje_id)\
        .filter(
            and_(
                Viaje.deleted_at.is_(None),
                GastoViaje.deleted_at.is_(None)
            )
        )
        
        if fecha_inicio:
            gastos_subquery = gastos_subquery.filter(Viaje.fecha_salida >= fecha_inicio)
        if fecha_fin:
            gastos_subquery = gastos_subquery.filter(Viaje.fecha_salida <= fecha_fin)
        
        gastos_result = gastos_subquery.group_by(Viaje.tipo_carga).all()
        gastos_dict = {g.tipo_carga: float(g.gasto_total_bs or 0) for g in gastos_result}
        
        # Combinar resultados
        reporte = []
        for r in result:
            gasto_total = gastos_dict.get(r.tipo_carga, 0)
            ingreso_total = float(r.ingreso_total_bs or 0)
            margen = ingreso_total - gasto_total
            
            reporte.append({
                "tipo_carga": r.tipo_carga,
                "total_viajes": r.total_viajes,
                "peso_total_ton": float(r.peso_total_ton or 0),
                "ingreso_total_bs": ingreso_total,
                "gasto_total_bs": gasto_total,
                "margen_bs": margen,
                "rentabilidad_porcentaje": (margen / ingreso_total * 100) if ingreso_total > 0 else 0
            })
        
        return sorted(reporte, key=lambda x: x['ingreso_total_bs'], reverse=True)
    
    def actualizar_estado(self, viaje_id: int, nuevo_estado: str) -> bool:
        """Actualizar estado de un viaje"""
        viaje = self.get_by_id(viaje_id)
        if not viaje:
            return False
        
        # Validar transiciones de estado
        transiciones_validas = {
            "PLANIFICADO": ["EN_RUTA"],
            "EN_RUTA": ["ENTREGADO"],
            "ENTREGADO": ["LIQUIDADO"],
            "LIQUIDADO": []  # Estado final
        }
        
        if nuevo_estado not in transiciones_validas.get(viaje.estado, []):
            return False
        
        viaje.estado = nuevo_estado
        viaje.updated_at = datetime.utcnow()
        
        # Si se marca como entregado y no tiene fecha de llegada, asignar fecha actual
        if nuevo_estado == "ENTREGADO" and not viaje.fecha_llegada:
            viaje.fecha_llegada = datetime.utcnow()
        
        self.db.commit()
        return True
    
    def cerrar_viaje(self, viaje_id: int, fecha_llegada: datetime, km_real: int, notas: str = None) -> bool:
        """Cerrar un viaje marcándolo como entregado"""
        viaje = self.get_by_id(viaje_id)
        if not viaje or viaje.estado not in ["PLANIFICADO", "EN_RUTA"]:
            return False
        
        viaje.fecha_llegada = fecha_llegada
        viaje.km_real = km_real
        if notas:
            viaje.notas = notas
        viaje.estado = "ENTREGADO"
        viaje.updated_at = datetime.utcnow()
        
        self.db.commit()
        return True
    
    def search_viajes(self, search_term: str) -> List[Viaje]:
        """Buscar viajes por origen, destino o tipo de carga"""
        return self.search(search_term, ['origen', 'destino', 'tipo_carga'])


class GastoViajeRepository(BaseRepository[GastoViaje]):
    """Repositorio para gestión de gastos de viajes"""
    
    def __init__(self, db: Session):
        super().__init__(db, GastoViaje)
    
    def get_by_viaje(self, viaje_id: int) -> List[GastoViaje]:
        """Obtener gastos de un viaje"""
        return self.db.query(GastoViaje).filter(
            and_(
                GastoViaje.viaje_id == viaje_id,
                GastoViaje.deleted_at.is_(None)
            )
        ).order_by(GastoViaje.fecha).all()
    
    def get_total_gastos_viaje(self, viaje_id: int) -> Decimal:
        """Obtener total de gastos de un viaje"""
        total = self.db.query(func.sum(GastoViaje.monto_bs)).filter(
            and_(
                GastoViaje.viaje_id == viaje_id,
                GastoViaje.deleted_at.is_(None)
            )
        ).scalar()
        
        return total or Decimal('0.00')
    
    def get_gastos_by_tipo(self, tipo: str, fecha_inicio: date = None, fecha_fin: date = None) -> List[GastoViaje]:
        """Obtener gastos por tipo en un período"""
        query = self.db.query(GastoViaje).filter(
            and_(
                GastoViaje.tipo == tipo,
                GastoViaje.deleted_at.is_(None)
            )
        )
        
        if fecha_inicio:
            query = query.filter(GastoViaje.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(GastoViaje.fecha <= fecha_fin)
        
        return query.all()
    
    def get_resumen_gastos_periodo(
        self, 
        fecha_inicio: date = None, 
        fecha_fin: date = None
    ) -> Dict[str, Decimal]:
        """Obtener resumen de gastos por tipo en un período"""
        query = self.db.query(
            GastoViaje.tipo,
            func.sum(GastoViaje.monto_bs).label('total')
        ).filter(GastoViaje.deleted_at.is_(None))
        
        if fecha_inicio:
            query = query.filter(GastoViaje.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(GastoViaje.fecha <= fecha_fin)
        
        result = query.group_by(GastoViaje.tipo).all()
        
        return {r.tipo: r.total for r in result}