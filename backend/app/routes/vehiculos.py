"""
Routes - Vehículos API
"""
from fastapi import APIRouter, Depends, Query, Path
from typing import Optional

from app.core.unit_of_work import UnitOfWork
from app.api.deps import get_uow, get_current_active_user
from app.services.vehiculos import VehiculoService
from app.models import Usuario

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])


def get_service(uow: UnitOfWork = Depends(get_uow)) -> VehiculoService:
    return VehiculoService(uow)


@router.get("")
async def listar(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    estado: Optional[str] = None,
    socio_id: Optional[int] = None,
    service: VehiculoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Listar vehículos con filtros"""
    return service.listar(page=page, limit=limit, estado=estado, socio_id=socio_id)


@router.get("/disponibles")
async def listar_disponibles(
    service: VehiculoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener vehículos disponibles"""
    return {"data": service.obtener_disponibles()}


@router.get("/{vehiculo_id}")
async def obtener(
    vehiculo_id: int = Path(...),
    service: VehiculoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener detalle de vehículo"""
    return {"data": service.obtener(vehiculo_id)}


@router.post("", status_code=201)
async def crear(
    datos: dict,
    service: VehiculoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear nuevo vehículo"""
    return {"data": service.crear(datos, current_user.id), "message": "Vehículo creado"}


@router.put("/{vehiculo_id}")
async def actualizar(
    vehiculo_id: int,
    datos: dict,
    service: VehiculoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar vehículo"""
    return {"data": service.actualizar(vehiculo_id, datos)}


@router.delete("/{vehiculo_id}")
async def eliminar(
    vehiculo_id: int,
    service: VehiculoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar vehículo"""
    service.eliminar(vehiculo_id)
    return {"success": True, "message": "Vehículo eliminado"}
