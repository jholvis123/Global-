"""
Routes - Anticipos API
"""
from fastapi import APIRouter, Depends, Query, Path
from typing import Optional
from datetime import date

from app.core.unit_of_work import UnitOfWork
from app.api.deps import get_uow, get_current_active_user
from app.application.services.anticipos import AnticipoService
from app.domain.entities import Usuario

router = APIRouter(prefix="/anticipos", tags=["Anticipos"])


def get_service(uow: UnitOfWork = Depends(get_uow)) -> AnticipoService:
    return AnticipoService(uow)


@router.get("")
async def listar(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    chofer_id: Optional[int] = None,
    estado: Optional[str] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    service: AnticipoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Listar anticipos con filtros"""
    return service.listar(
        page=page, 
        limit=limit, 
        chofer_id=chofer_id,
        estado=estado,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )


@router.get("/chofer/{chofer_id}/pendientes")
async def pendientes_chofer(
    chofer_id: int = Path(...),
    service: AnticipoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener anticipos pendientes de un chofer"""
    return service.obtener_pendientes_chofer(chofer_id)


@router.get("/{anticipo_id}")
async def obtener(
    anticipo_id: int = Path(...),
    service: AnticipoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener detalle de anticipo"""
    return {"data": service.obtener(anticipo_id)}


@router.post("", status_code=201)
async def crear(
    datos: dict,
    service: AnticipoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear nuevo anticipo"""
    return {"data": service.crear(datos, current_user.id), "message": "Anticipo creado"}


@router.delete("/{anticipo_id}")
async def eliminar(
    anticipo_id: int,
    service: AnticipoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Eliminar anticipo"""
    service.eliminar(anticipo_id)
    return {"success": True, "message": "Anticipo eliminado"}
