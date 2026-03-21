"""
Services - Viajes (Lógica principal)
"""
from typing import Optional, Dict, Any
from datetime import date, datetime
from decimal import Decimal

from app.core.unit_of_work import UnitOfWork
from app.domain.services import CalculadoraTarifa, ValidadorViaje
from app.domain.exceptions import (
    EntityNotFoundException,
    BusinessRuleException,
    InvalidStateTransitionException,
    ResourceNotAvailableException,
    ValidationException
)


class ViajeService:
    """Servicio de aplicación para gestión de viajes"""
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.calculadora = CalculadoraTarifa()
        self.validador = ValidadorViaje()
    
    def listar(
        self,
        page: int = 1,
        limit: int = 20,
        estado: Optional[str] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        cliente_id: Optional[int] = None,
        vehiculo_id: Optional[int] = None,
        chofer_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Listar viajes con filtros y paginación"""
        with self.uow:
            filtros = {}
            if estado:
                filtros["estado"] = estado
            if cliente_id:
                filtros["cliente_id"] = cliente_id
            if vehiculo_id:
                filtros["vehiculo_id"] = vehiculo_id
            if chofer_id:
                filtros["chofer_id"] = chofer_id
            
            viajes = self.uow.viajes.get_all(
                skip=(page - 1) * limit,
                limit=limit,
                filters=filtros
            )
            total = self.uow.viajes.count(filtros)
            
            # Estadísticas
            estadisticas = self._calcular_estadisticas(viajes)
            
            return {
                "data": [self._to_resumen(v) for v in viajes],
                "total": total,
                "page": page,
                "limit": limit,
                "estadisticas": estadisticas
            }
    
    def obtener(self, viaje_id: int) -> Dict[str, Any]:
        """Obtener detalle completo de un viaje"""
        with self.uow:
            viaje = self.uow.viajes.get_with_relations(viaje_id)
            if not viaje:
                raise EntityNotFoundException("Viaje", viaje_id)
            return self._to_detalle(viaje)
    
    def crear(self, datos: Dict[str, Any], usuario_id: int) -> Dict[str, Any]:
        """Crear nuevo viaje con validaciones"""
        with self.uow:
            # Validar datos
            errores = self.validador.validar_creacion(
                origen=datos.get("origen"),
                destino=datos.get("destino"),
                peso_ton=Decimal(str(datos.get("peso_ton", 0))),
                km_estimado=datos.get("km_estimado", 0),
                tarifa_tipo=datos.get("tarifa_tipo"),
                tarifa_valor=Decimal(str(datos.get("tarifa_valor", 0))),
                tipo_carga=datos.get("tipo_carga")
            )
            if errores:
                raise ValidationException("datos", "; ".join(errores))
            
            # Verificar recursos disponibles
            vehiculo = self.uow.vehiculos.get_by_id(datos["vehiculo_id"])
            if not vehiculo:
                raise EntityNotFoundException("Vehículo", datos["vehiculo_id"])
            if vehiculo.estado != "DISPONIBLE":
                raise ResourceNotAvailableException("Vehículo", datos["vehiculo_id"])
            
            chofer = self.uow.choferes.get_by_id(datos["chofer_id"])
            if not chofer:
                raise EntityNotFoundException("Chofer", datos["chofer_id"])
            if chofer.estado != "DISPONIBLE":
                raise ResourceNotAvailableException("Chofer", datos["chofer_id"])
            
            cliente = self.uow.clientes.get_by_id(datos["cliente_id"])
            if not cliente:
                raise EntityNotFoundException("Cliente", datos["cliente_id"])
            
            # Calcular ingreso estimado
            ingreso = self.calculadora.calcular_ingreso(
                datos["tarifa_tipo"],
                Decimal(str(datos["tarifa_valor"])),
                Decimal(str(datos["peso_ton"])),
                datos["km_estimado"]
            )
            
            # Crear viaje
            viaje = self.uow.viajes.create({
                **datos,
                "estado": "PLANIFICADO",
                "ingreso_estimado_bs": float(ingreso.valor)
            })
            
            # Reservar recursos
            self.uow.vehiculos.actualizar_estado(vehiculo.id, "RESERVADO")
            self.uow.choferes.actualizar_estado(chofer.id, "ASIGNADO")
            
            self.uow.commit()
            return self._to_detalle(viaje)
    
    def iniciar(self, viaje_id: int, usuario_id: int) -> Dict[str, Any]:
        """Iniciar viaje (PLANIFICADO -> EN_RUTA)"""
        with self.uow:
            viaje = self.uow.viajes.get_by_id(viaje_id)
            if not viaje:
                raise EntityNotFoundException("Viaje", viaje_id)
            
            if not self.validador.puede_cambiar_estado(viaje.estado, "EN_RUTA"):
                raise InvalidStateTransitionException("Viaje", viaje.estado, "EN_RUTA")
            
            self.uow.viajes.update(viaje_id, {
                "estado": "EN_RUTA",
                "fecha_inicio_real": datetime.utcnow()
            })
            
            self.uow.vehiculos.actualizar_estado(viaje.vehiculo_id, "EN_VIAJE")
            self.uow.choferes.actualizar_estado(viaje.chofer_id, "EN_VIAJE")
            
            self.uow.commit()
            return self.obtener(viaje_id)
    
    def finalizar(self, viaje_id: int, km_real: int, usuario_id: int) -> Dict[str, Any]:
        """Finalizar viaje (EN_RUTA -> ENTREGADO)"""
        with self.uow:
            viaje = self.uow.viajes.get_with_relations(viaje_id)
            if not viaje:
                raise EntityNotFoundException("Viaje", viaje_id)
            
            errores = self.validador.validar_finalizacion(viaje.estado, km_real)
            if errores:
                raise BusinessRuleException("; ".join(errores))
            
            # Recalcular ingreso
            ingreso = self.calculadora.calcular_ingreso(
                viaje.tarifa_tipo,
                viaje.tarifa_valor,
                viaje.peso_ton,
                km_real
            )
            
            self.uow.viajes.update(viaje_id, {
                "estado": "ENTREGADO",
                "km_real": km_real,
                "fecha_llegada": datetime.utcnow(),
                "ingreso_real_bs": float(ingreso.valor)
            })
            
            self.uow.vehiculos.actualizar_estado(viaje.vehiculo_id, "DISPONIBLE")
            self.uow.choferes.actualizar_estado(viaje.chofer_id, "DISPONIBLE")
            
            self.uow.commit()
            return self.obtener(viaje_id)
    
    def _calcular_estadisticas(self, viajes) -> Dict[str, Any]:
        """Calcular estadísticas de viajes"""
        if not viajes:
            return {"total_ingresos_bs": 0, "total_gastos_bs": 0}
        
        return {
            "total_ingresos_bs": sum(float(v.ingreso_total_bs) for v in viajes),
            "total_gastos_bs": sum(float(v.total_gastos_bs) for v in viajes),
            "total_viajes": len(viajes)
        }
    
    def _to_resumen(self, v) -> Dict[str, Any]:
        """Viaje a resumen para listado"""
        return {
            "id": v.id,
            "ruta": f"{v.origen} → {v.destino}",
            "cliente": v.cliente.nombre if v.cliente else None,
            "vehiculo": v.vehiculo.placa if v.vehiculo else None,
            "chofer": f"{v.chofer.nombre} {v.chofer.apellido}" if v.chofer else None,
            "fecha_salida": str(v.fecha_salida),
            "estado": v.estado,
            "ingreso_bs": float(v.ingreso_total_bs),
            "margen_bs": float(v.margen_bruto_bs)
        }
    
    def _to_detalle(self, v) -> Dict[str, Any]:
        """Viaje a detalle completo"""
        return {
            **self._to_resumen(v),
            "fecha_llegada": str(v.fecha_llegada) if v.fecha_llegada else None,
            "tipo_carga": v.tipo_carga,
            "peso_ton": float(v.peso_ton),
            "km_estimado": v.km_estimado,
            "km_real": v.km_real,
            "tarifa_tipo": v.tarifa_tipo,
            "tarifa_valor": float(v.tarifa_valor),
            "gastos_bs": float(v.total_gastos_bs),
            "notas": v.notas
        }
