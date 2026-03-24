
from fastapi import APIRouter, Depends, Query, Path
from typing import Optional
from datetime import date

from app.api.deps import get_viaje_service, get_current_active_user
from app.application.services.viaje_service import ViajeService
from app.api.schemas.responses import (
    PaginatedResponse,
    DataResponse,
    BaseResponse,
    ViajeResumen,
    ViajeDetalle,
    EstadisticasViajes
)
from app.api.schemas.viaje import ViajeCreate, ViajeUpdate
from app.domain.entities import Usuario


router = APIRouter(prefix="/viajes", tags=["Viajes"])


# ==================== LISTADO Y CONSULTAS ====================

@router.get("", response_model=PaginatedResponse[ViajeResumen])
async def listar_viajes(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(20, ge=1, le=100, description="Registros por página"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicio del período"),
    fecha_fin: Optional[date] = Query(None, description="Fecha fin del período"),
    cliente_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    vehiculo_id: Optional[int] = Query(None, description="Filtrar por vehículo"),
    chofer_id: Optional[int] = Query(None, description="Filtrar por chofer"),
    orden: str = Query("fecha_salida", description="Campo para ordenar"),
    direccion: str = Query("desc", pattern="^(asc|desc)$", description="Dirección del orden"),
    service: ViajeService = Depends(get_viaje_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Listar viajes con filtros y paginación.
    
    Retorna lista de viajes con:
    - Paginación completa
    - Estadísticas del conjunto filtrado
    - Filtros aplicados
    
    **Permisos**: Usuario autenticado
    """
    return service.listar_viajes(
        page=page,
        limit=limit,
        estado=estado,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        cliente_id=cliente_id,
        vehiculo_id=vehiculo_id,
        chofer_id=chofer_id,
        orden=orden,
        direccion=direccion
    )


@router.get("/estadisticas", response_model=DataResponse[EstadisticasViajes])
async def obtener_estadisticas(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    service: ViajeService = Depends(get_viaje_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtener estadísticas generales de viajes.
    
    **Permisos**: Usuario autenticado
    """
    stats = service.obtener_estadisticas_dashboard()
    return DataResponse(data=stats)


@router.get("/{viaje_id}", response_model=DataResponse[ViajeDetalle])
async def obtener_viaje(
    viaje_id: int = Path(..., description="ID del viaje"),
    service: ViajeService = Depends(get_viaje_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtener detalle completo de un viaje.
    
    Incluye:
    - Información del cliente, vehículo y chofer
    - Lista de gastos
    - Liquidación (si existe)
    
    **Permisos**: Usuario autenticado
    """
    viaje = service.obtener_viaje(viaje_id)
    return DataResponse(data=viaje)


# ==================== CREAR Y MODIFICAR ====================

@router.post("", response_model=DataResponse[ViajeDetalle], status_code=201)
async def crear_viaje(
    viaje_data: ViajeCreate,
    service: ViajeService = Depends(get_viaje_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Crear nuevo viaje.
    
    El sistema automáticamente:
    - Valida disponibilidad de vehículo y chofer
    - Calcula ingreso estimado según tarifa
    - Actualiza estados de recursos
    
    **Permisos**: Usuario autenticado
    """
    viaje = service.crear_viaje(viaje_data.model_dump(), current_user.id)
    return DataResponse(
        data=viaje,
        message="Viaje creado exitosamente"
    )


@router.put("/{viaje_id}", response_model=DataResponse[ViajeDetalle])
async def actualizar_viaje(
    viaje_id: int,
    viaje_data: ViajeUpdate,
    service: ViajeService = Depends(get_viaje_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Actualizar datos de un viaje.
    
    Solo se pueden actualizar viajes en estado PLANIFICADO o EN_RUTA.
    
    **Permisos**: Usuario autenticado
    """
    # TODO: Implementar actualización
    pass


@router.delete("/{viaje_id}", response_model=BaseResponse)
async def eliminar_viaje(
    viaje_id: int,
    service: ViajeService = Depends(get_viaje_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Eliminar viaje (soft delete).
    
    Solo se pueden eliminar viajes en estado PLANIFICADO.
    
    **Permisos**: Usuario autenticado
    """
    # TODO: Implementar eliminación
    pass


# ==================== ACCIONES DE ESTADO ====================

@router.post("/{viaje_id}/iniciar", response_model=DataResponse[ViajeDetalle])
async def iniciar_viaje(
    viaje_id: int = Path(..., description="ID del viaje"),
    service: ViajeService = Depends(get_viaje_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Iniciar un viaje (cambiar estado a EN_RUTA).
    
    Requisitos:
    - Viaje debe estar en estado PLANIFICADO
    - Vehículo y chofer deben estar disponibles
    
    **Permisos**: Usuario autenticado
    """
    viaje = service.iniciar_viaje(viaje_id, current_user.id)
    return DataResponse(
        data=viaje,
        message="Viaje iniciado exitosamente"
    )


@router.post("/{viaje_id}/finalizar", response_model=DataResponse[ViajeDetalle])
async def finalizar_viaje(
    viaje_id: int = Path(..., description="ID del viaje"),
    km_real: int = Query(..., gt=0, description="Kilómetros reales recorridos"),
    service: ViajeService = Depends(get_viaje_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Finalizar un viaje (cambiar estado a ENTREGADO).
    
    El sistema automáticamente:
    - Recalcula ingreso con kilómetros reales
    - Libera vehículo y chofer
    - Registra fecha de llegada
    
    **Permisos**: Usuario autenticado
    """
    viaje = service.finalizar_viaje(viaje_id, km_real, current_user.id)
    return DataResponse(
        data=viaje,
        message="Viaje finalizado exitosamente"
    )


# ==================== GASTOS ====================

@router.post("/{viaje_id}/gastos", response_model=BaseResponse, status_code=201)
async def agregar_gasto(
    viaje_id: int = Path(..., description="ID del viaje"),
    tipo: str = Query(..., description="Tipo de gasto"),
    monto_bs: float = Query(..., gt=0, description="Monto en Bs"),
    descripcion: Optional[str] = Query(None, description="Descripción del gasto"),
    service: ViajeService = Depends(get_viaje_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Agregar un gasto a un viaje.
    
    Tipos válidos: COMBUSTIBLE, PEAJE, VIATICO, TALLER, OTRO
    
    **Permisos**: Usuario autenticado
    """
    result = service.agregar_gasto(
        viaje_id=viaje_id,
        tipo=tipo,
        monto_bs=monto_bs,
        descripcion=descripcion,
        usuario_id=current_user.id
    )
    return BaseResponse(message=result["message"])


@router.get("/{viaje_id}/gastos")
async def listar_gastos_viaje(
    viaje_id: int = Path(..., description="ID del viaje"),
    service: ViajeService = Depends(get_viaje_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Listar gastos de un viaje.
    
    **Permisos**: Usuario autenticado
    """
    # TODO: Implementar
    pass
