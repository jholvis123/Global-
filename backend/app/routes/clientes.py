"""
Routes - Clientes API
"""
from fastapi import APIRouter, Depends, Query, Path
from typing import Optional

from app.core.unit_of_work import UnitOfWork
from app.api.deps import get_uow, get_current_active_user
from app.services.clientes import ClienteService
from app.models import Usuario

router = APIRouter(prefix="/clientes", tags=["Clientes"])


def get_service(uow: UnitOfWork = Depends(get_uow)) -> ClienteService:
    return ClienteService(uow)


@router.get("")
async def listar(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    estado: Optional[str] = None,
    busqueda: Optional[str] = None,
    service: ClienteService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Listar clientes con filtros"""
    return service.listar(page=page, limit=limit, estado=estado, busqueda=busqueda)


@router.get("/activos")
async def listar_activos(
    service: ClienteService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener clientes activos para selects"""
    return {"data": service.obtener_activos()}


@router.get("/{cliente_id}")
async def obtener(
    cliente_id: int = Path(...),
    service: ClienteService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener detalle de cliente"""
    return {"data": service.obtener(cliente_id)}


@router.post("", status_code=201)
async def crear(
    datos: dict,
    service: ClienteService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear nuevo cliente"""
    return {"data": service.crear(datos, current_user.id), "message": "Cliente creado"}


@router.put("/{cliente_id}")
async def actualizar(
    cliente_id: int,
    datos: dict,
    service: ClienteService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar cliente"""
    return {"data": service.actualizar(cliente_id, datos)}


@router.delete("/{cliente_id}")
async def eliminar(
    cliente_id: int,
    service: ClienteService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar cliente"""
    service.eliminar(cliente_id)
    return {"success": True, "message": "Cliente eliminado"}
