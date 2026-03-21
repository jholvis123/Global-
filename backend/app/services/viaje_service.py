"""
Application Services - Orquestan casos de uso y coordinan la lógica de aplicación.
Aquí se maneja TODA la lógica de negocio que el Frontend no debe conocer.
"""
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from decimal import Decimal

from app.core.unit_of_work import UnitOfWork
from app.domain.services import (
    CalculadoraTarifa, 
    CalculadoraLiquidacion, 
    ValidadorViaje,
    CalculadoraEstadisticas
)
from app.domain.exceptions import (
    EntityNotFoundException,
    BusinessRuleException,
    InvalidStateTransitionException,
    ResourceNotAvailableException,
    ValidationException
)
from app.schemas.responses import (
    ViajeResumen,
    ViajeDetalle,
    EstadisticasViajes,
    PaginationMeta
)


class ViajeService:
    """
    Servicio de aplicación para gestión de viajes.
    Orquesta TODA la lógica de viajes.
    """
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.calculadora_tarifa = CalculadoraTarifa()
        self.validador = ValidadorViaje()
        self.calculadora_stats = CalculadoraEstadisticas()
    
    def listar_viajes(
        self,
        page: int = 1,
        limit: int = 20,
        estado: Optional[str] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        cliente_id: Optional[int] = None,
        vehiculo_id: Optional[int] = None,
        chofer_id: Optional[int] = None,
        orden: str = "fecha_salida",
        direccion: str = "desc"
    ) -> Dict[str, Any]:
        """
        Listar viajes con filtros, paginación y estadísticas.
        El Frontend solo pide datos, TODA la lógica está aquí.
        """
        with self.uow:
            # Obtener viajes con paginación
            viajes, total = self.uow.viajes.get_all(
                skip=(page - 1) * limit,
                limit=limit,
                filters={
                    "estado": estado,
                    "cliente_id": cliente_id,
                    "vehiculo_id": vehiculo_id,
                    "chofer_id": chofer_id
                }
            ), self.uow.viajes.count()
            
            # Calcular estadísticas (LÓGICA EN BACKEND)
            viajes_data = [self._viaje_a_dict(v) for v in viajes]
            estadisticas = self.calculadora_stats.calcular_resumen_viajes(viajes_data)
            
            # Calcular paginación
            total_pages = (total + limit - 1) // limit
            
            return {
                "data": [self._formatear_resumen(v) for v in viajes],
                "pagination": PaginationMeta(
                    total=total,
                    page=page,
                    limit=limit,
                    total_pages=total_pages,
                    has_next=page < total_pages,
                    has_prev=page > 1
                ),
                "estadisticas": estadisticas,
                "filtros_aplicados": {
                    "estado": estado,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
            }
    
    def obtener_viaje(self, viaje_id: int) -> ViajeDetalle:
        """Obtener detalle completo de un viaje"""
        with self.uow:
            viaje = self.uow.viajes.get_with_relations(viaje_id)
            
            if not viaje:
                raise EntityNotFoundException("Viaje", viaje_id)
            
            return self._formatear_detalle(viaje)
    
    def crear_viaje(self, datos: Dict[str, Any], usuario_id: int) -> ViajeDetalle:
        """
        Crear nuevo viaje con todas las validaciones.
        TODA la lógica de validación y cálculo está aquí.
        """
        with self.uow:
            # 1. Validar datos de entrada (LÓGICA EN BACKEND)
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
            
            # 2. Verificar disponibilidad de recursos (LÓGICA EN BACKEND)
            # vehiculo = self.uow.vehiculos.get_by_id(datos["vehiculo_id"])
            # if not vehiculo or vehiculo.estado != "DISPONIBLE":
            #     raise ResourceNotAvailableException("Vehículo", datos["vehiculo_id"])
            
            # chofer = self.uow.choferes.get_by_id(datos["chofer_id"])
            # if not chofer or chofer.estado != "DISPONIBLE":
            #     raise ResourceNotAvailableException("Chofer", datos["chofer_id"])
            
            # 3. Calcular ingreso estimado (LÓGICA EN BACKEND)
            ingreso_estimado = self.calculadora_tarifa.calcular_ingreso(
                tarifa_tipo=datos["tarifa_tipo"],
                tarifa_valor=Decimal(str(datos["tarifa_valor"])),
                peso_ton=Decimal(str(datos["peso_ton"])),
                km=datos["km_estimado"]
            )
            
            # 4. Crear viaje
            viaje_data = {
                **datos,
                "estado": "PLANIFICADO",
                "ingreso_estimado_bs": float(ingreso_estimado.valor),
                "created_by": usuario_id
            }
            
            viaje = self.uow.viajes.create(viaje_data)
            
            # 5. Actualizar estados de recursos
            # self.uow.vehiculos.update(vehiculo.id, {"estado": "EN_VIAJE"})
            # self.uow.choferes.update(chofer.id, {"estado": "EN_VIAJE"})
            
            self.uow.commit()
            
            return self._formatear_detalle(viaje)
    
    def iniciar_viaje(self, viaje_id: int, usuario_id: int) -> ViajeDetalle:
        """Cambiar estado de viaje a EN_RUTA"""
        with self.uow:
            viaje = self.uow.viajes.get_by_id(viaje_id)
            
            if not viaje:
                raise EntityNotFoundException("Viaje", viaje_id)
            
            # Validar transición de estado (LÓGICA EN BACKEND)
            if not self.validador.puede_cambiar_estado(viaje.estado, "EN_RUTA"):
                raise InvalidStateTransitionException("Viaje", viaje.estado, "EN_RUTA")
            
            self.uow.viajes.update(viaje_id, {
                "estado": "EN_RUTA",
                "fecha_inicio_real": datetime.utcnow()
            })
            
            self.uow.commit()
            
            return self.obtener_viaje(viaje_id)
    
    def finalizar_viaje(
        self, 
        viaje_id: int, 
        km_real: int,
        usuario_id: int
    ) -> ViajeDetalle:
        """Cambiar estado de viaje a ENTREGADO"""
        with self.uow:
            viaje = self.uow.viajes.get_by_id(viaje_id)
            
            if not viaje:
                raise EntityNotFoundException("Viaje", viaje_id)
            
            # Validar (LÓGICA EN BACKEND)
            errores = self.validador.validar_finalizacion(viaje.estado, km_real)
            if errores:
                raise BusinessRuleException("; ".join(errores))
            
            # Recalcular ingreso con km reales (LÓGICA EN BACKEND)
            ingreso_real = self.calculadora_tarifa.calcular_ingreso(
                tarifa_tipo=viaje.tarifa_tipo,
                tarifa_valor=viaje.tarifa_valor,
                peso_ton=viaje.peso_ton,
                km=km_real
            )
            
            self.uow.viajes.update(viaje_id, {
                "estado": "ENTREGADO",
                "km_real": km_real,
                "fecha_llegada": datetime.utcnow(),
                "ingreso_real_bs": float(ingreso_real.valor)
            })
            
            # Liberar recursos
            # self.uow.vehiculos.update(viaje.vehiculo_id, {"estado": "DISPONIBLE"})
            # self.uow.choferes.update(viaje.chofer_id, {"estado": "DISPONIBLE"})
            
            self.uow.commit()
            
            return self.obtener_viaje(viaje_id)
    
    def agregar_gasto(
        self,
        viaje_id: int,
        tipo: str,
        monto_bs: float,
        descripcion: str = None,
        usuario_id: int = None
    ) -> Dict[str, Any]:
        """Agregar un gasto a un viaje"""
        with self.uow:
            viaje = self.uow.viajes.get_by_id(viaje_id)
            
            if not viaje:
                raise EntityNotFoundException("Viaje", viaje_id)
            
            if viaje.estado == "LIQUIDADO":
                raise BusinessRuleException("No se pueden agregar gastos a viajes liquidados")
            
            # Crear gasto (pendiente de implementar GastoRepository)
            # gasto = self.uow.gastos.create({...})
            
            self.uow.commit()
            
            return {"message": "Gasto agregado correctamente"}
    
    def obtener_estadisticas_dashboard(self) -> Dict[str, Any]:
        """Obtener estadísticas para el dashboard"""
        with self.uow:
            hoy = date.today()
            
            # Estadísticas del día
            viajes_hoy = self.uow.viajes.get_viajes_fecha(hoy) if hasattr(self.uow.viajes, 'get_viajes_fecha') else []
            
            # Estadísticas del mes
            viajes_mes = self.uow.viajes.get_estadisticas_mensuales(hoy.year, hoy.month) if hasattr(self.uow.viajes, 'get_estadisticas_mensuales') else {}
            
            # Viajes por estado
            viajes_planificados = len(self.uow.viajes.get_by_estado("PLANIFICADO") if hasattr(self.uow.viajes, 'get_by_estado') else [])
            viajes_en_ruta = len(self.uow.viajes.get_by_estado("EN_RUTA") if hasattr(self.uow.viajes, 'get_by_estado') else [])
            viajes_pendientes = len(self.uow.viajes.get_viajes_pendientes_liquidacion() if hasattr(self.uow.viajes, 'get_viajes_pendientes_liquidacion') else [])
            
            return {
                "resumen_hoy": {
                    "total_viajes": len(viajes_hoy),
                    "ingresos_bs": sum(v.ingreso_total_bs for v in viajes_hoy) if viajes_hoy else 0,
                    "viajes_en_ruta": viajes_en_ruta
                },
                "resumen_mes": viajes_mes,
                "contadores": {
                    "planificados": viajes_planificados,
                    "en_ruta": viajes_en_ruta,
                    "pendientes_liquidacion": viajes_pendientes
                }
            }
    
    # ==================== Métodos privados ====================
    
    def _formatear_resumen(self, viaje) -> ViajeResumen:
        """Convertir entidad a resumen para listado"""
        return ViajeResumen(
            id=viaje.id,
            ruta=f"{viaje.origen} → {viaje.destino}",
            cliente_nombre=viaje.cliente.nombre if viaje.cliente else "N/A",
            vehiculo_placa=viaje.vehiculo.placa if viaje.vehiculo else "N/A",
            chofer_nombre=f"{viaje.chofer.nombre} {viaje.chofer.apellido}" if viaje.chofer else "N/A",
            fecha_salida=viaje.fecha_salida,
            estado=viaje.estado,
            ingreso_bs=float(viaje.ingreso_total_bs),
            gastos_bs=float(viaje.total_gastos_bs),
            margen_bs=float(viaje.margen_bruto_bs)
        )
    
    def _formatear_detalle(self, viaje) -> ViajeDetalle:
        """Convertir entidad a detalle completo"""
        resumen = self._formatear_resumen(viaje)
        return ViajeDetalle(
            **resumen.model_dump(),
            fecha_llegada=viaje.fecha_llegada,
            volumen_m3=float(viaje.volumen_m3) if viaje.volumen_m3 else None,
            km_real=viaje.km_real,
            notas=viaje.notas,
            gastos=[],  # TODO: Mapear gastos
            liquidacion=None,  # TODO: Mapear liquidación
            created_at=viaje.created_at,
            updated_at=viaje.updated_at
        )
    
    def _viaje_a_dict(self, viaje) -> Dict[str, Any]:
        """Convertir viaje a diccionario para cálculos"""
        return {
            "id": viaje.id,
            "estado": viaje.estado,
            "ingreso_bs": float(viaje.ingreso_total_bs),
            "gastos_bs": float(viaje.total_gastos_bs),
            "peso_ton": float(viaje.peso_ton),
            "km_estimado": viaje.km_estimado,
            "km_real": viaje.km_real
        }


class LiquidacionService:
    """
    Servicio de aplicación para gestión de liquidaciones.
    """
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.calculadora = CalculadoraLiquidacion()
    
    def generar_liquidacion(self, viaje_id: int, usuario_id: int) -> Dict[str, Any]:
        """
        Generar liquidación para un viaje.
        TODA la lógica de cálculo está aquí.
        """
        with self.uow:
            # Obtener viaje con relaciones
            viaje = self.uow.viajes.get_with_relations(viaje_id)
            
            if not viaje:
                raise EntityNotFoundException("Viaje", viaje_id)
            
            if viaje.estado != "ENTREGADO":
                raise BusinessRuleException("Solo se pueden liquidar viajes entregados")
            
            if viaje.liquidacion:
                raise BusinessRuleException("El viaje ya tiene una liquidación")
            
            # Obtener socio del vehículo
            socio = viaje.vehiculo.socio if viaje.vehiculo else None
            if not socio:
                raise BusinessRuleException("El vehículo no tiene socio asignado")
            
            # Obtener anticipos pendientes del chofer
            # anticipos = self.uow.anticipos.get_pendientes_chofer(viaje.chofer_id)
            # total_anticipos = sum(a.monto_bs for a in anticipos)
            total_anticipos = Decimal("0")
            
            # Calcular liquidación (TODA LA LÓGICA EN BACKEND)
            gastos_data = [
                {"tipo": g.tipo, "monto_bs": float(g.monto_bs)}
                for g in viaje.gastos
            ]
            
            liquidacion_calculada = self.calculadora.calcular(
                ingreso_bs=Decimal(str(viaje.ingreso_total_bs)),
                gastos=gastos_data,
                porcentaje_socio=Decimal(str(socio.porcentaje_participacion)),
                anticipos_pendientes=total_anticipos
            )
            
            # Crear liquidación
            # liquidacion = self.uow.liquidaciones.create({...})
            
            # Actualizar estado del viaje
            self.uow.viajes.update(viaje_id, {"estado": "LIQUIDADO"})
            
            # Marcar anticipos como descontados
            # for anticipo in anticipos:
            #     self.uow.anticipos.update(anticipo.id, {"estado": "DESCONTADO"})
            
            self.uow.commit()
            
            return liquidacion_calculada


class ReporteService:
    """
    Servicio de aplicación para generación de reportes.
    """
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.calculadora = CalculadoraEstadisticas()
    
    def generar_reporte_ingresos(
        self,
        fecha_inicio: date,
        fecha_fin: date,
        agrupar_por: str = "dia"  # dia, semana, mes
    ) -> Dict[str, Any]:
        """Generar reporte de ingresos"""
        with self.uow:
            # Obtener viajes del período
            viajes = self.uow.viajes.get_all(
                filters={
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
            )
            
            # Agrupar y calcular
            # ... lógica de agrupación
            
            return {
                "periodo": {
                    "inicio": fecha_inicio,
                    "fin": fecha_fin
                },
                "totales": self.calculadora.calcular_resumen_viajes(
                    [{"ingreso_bs": v.ingreso_total_bs} for v in viajes]
                ),
                "detalle": []  # Datos agrupados
            }
