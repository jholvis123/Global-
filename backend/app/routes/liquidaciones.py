"""
Routes - Liquidaciones API
"""
from fastapi import APIRouter, Depends, Query, Path
from typing import Optional
from datetime import date

from app.core.unit_of_work import UnitOfWork
from app.api.deps import get_uow, get_current_active_user
from app.services.liquidaciones import LiquidacionService
from app.models import Usuario

router = APIRouter(prefix="/liquidaciones", tags=["Liquidaciones"])


def get_service(uow: UnitOfWork = Depends(get_uow)) -> LiquidacionService:
    return LiquidacionService(uow)


@router.get("")
async def listar(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    service: LiquidacionService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Listar liquidaciones con filtros"""
    return service.listar(
        page=page, 
        limit=limit, 
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )


@router.get("/pendientes")
async def viajes_pendientes(
    service: LiquidacionService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener viajes pendientes de liquidación"""
    return {"data": service.obtener_pendientes()}


@router.get("/{liquidacion_id}")
async def obtener(
    liquidacion_id: int = Path(...),
    service: LiquidacionService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener detalle de liquidación"""
    return {"data": service.obtener(liquidacion_id)}


@router.post("/viaje/{viaje_id}", status_code=201)
async def generar(
    viaje_id: int = Path(...),
    service: LiquidacionService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Generar liquidación para un viaje"""
    return {
        "data": service.generar(viaje_id, current_user.id), 
        "message": "Liquidación generada"
    }
