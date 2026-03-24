"""
Routes - Choferes API
"""
from fastapi import APIRouter, Depends, Query, Path
from typing import Optional

from app.core.unit_of_work import UnitOfWork
from app.api.deps import get_uow, get_current_active_user
from app.application.services.choferes import ChoferService
from app.domain.entities import Usuario

router = APIRouter(prefix="/choferes", tags=["Choferes"])


def get_service(uow: UnitOfWork = Depends(get_uow)) -> ChoferService:
    return ChoferService(uow)


@router.get("")
async def listar(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    estado: Optional[str] = None,
    busqueda: Optional[str] = None,
    service: ChoferService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Listar choferes con filtros"""
    return service.listar(page=page, limit=limit, estado=estado, busqueda=busqueda)


@router.get("/disponibles")
async def listar_disponibles(
    service: ChoferService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener choferes disponibles"""
    return {"data": service.obtener_disponibles()}


@router.get("/{chofer_id}")
async def obtener(
    chofer_id: int = Path(...),
    service: ChoferService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener detalle de chofer"""
    return {"data": service.obtener(chofer_id)}


@router.post("", status_code=201)
async def crear(
    datos: dict,
    service: ChoferService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear nuevo chofer"""
    return {"data": service.crear(datos, current_user.id), "message": "Chofer creado"}


@router.put("/{chofer_id}")
async def actualizar(
    chofer_id: int,
    datos: dict,
    service: ChoferService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar chofer"""
    return {"data": service.actualizar(chofer_id, datos)}


@router.delete("/{chofer_id}")
async def eliminar(
    chofer_id: int,
    service: ChoferService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar chofer"""
    service.eliminar(chofer_id)
    return {"success": True, "message": "Chofer eliminado"}
