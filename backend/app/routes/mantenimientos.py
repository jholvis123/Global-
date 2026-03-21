"""
Routes - Mantenimientos API
"""
from fastapi import APIRouter, Depends, Query, Path
from typing import Optional

from app.core.unit_of_work import UnitOfWork
from app.api.deps import get_uow, get_current_active_user
from app.services.mantenimientos import MantenimientoService
from app.models import Usuario

router = APIRouter(prefix="/mantenimientos", tags=["Mantenimientos"])


def get_service(uow: UnitOfWork = Depends(get_uow)) -> MantenimientoService:
    return MantenimientoService(uow)


@router.get("")
async def listar(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    vehiculo_id: Optional[int] = None,
    estado: Optional[str] = None,
    tipo: Optional[str] = None,
    service: MantenimientoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Listar mantenimientos con filtros"""
    return service.listar(
        page=page, 
        limit=limit, 
        vehiculo_id=vehiculo_id,
        estado=estado,
        tipo=tipo
    )


@router.get("/proximos")
async def proximos(
    dias: int = Query(30, ge=1, le=90),
    service: MantenimientoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener mantenimientos programados próximos"""
    return {"data": service.obtener_proximos(dias)}


@router.get("/vehiculo/{vehiculo_id}/historial")
async def historial_vehiculo(
    vehiculo_id: int = Path(...),
    service: MantenimientoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener historial de mantenimientos de un vehículo"""
    return service.obtener_historial_vehiculo(vehiculo_id)


@router.get("/{mant_id}")
async def obtener(
    mant_id: int = Path(...),
    service: MantenimientoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener detalle de mantenimiento"""
    return {"data": service.obtener(mant_id)}


@router.post("", status_code=201)
async def crear(
    datos: dict,
    service: MantenimientoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear nuevo mantenimiento"""
    return {"data": service.crear(datos, current_user.id), "message": "Mantenimiento creado"}


@router.put("/{mant_id}")
async def actualizar(
    mant_id: int,
    datos: dict,
    service: MantenimientoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar mantenimiento"""
    return {"data": service.actualizar(mant_id, datos)}


@router.post("/{mant_id}/completar")
async def completar(
    mant_id: int = Path(...),
    costo_bs: float = Query(..., gt=0),
    notas: Optional[str] = None,
    service: MantenimientoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Marcar mantenimiento como completado"""
    return {
        "data": service.completar(mant_id, costo_bs, notas),
        "message": "Mantenimiento completado"
    }
