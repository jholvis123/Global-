"""
Routes - Dashboard y Reportes API
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import date

from app.core.unit_of_work import UnitOfWork
from app.api.deps import get_uow, get_current_active_user
from app.application.services.viajes import ViajeEstadisticasService
from app.domain.entities import Usuario

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_service(uow: UnitOfWork = Depends(get_uow)) -> ViajeEstadisticasService:
    return ViajeEstadisticasService(uow)


@router.get("")
async def dashboard(
    service: ViajeEstadisticasService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener datos del dashboard principal"""
    return service.dashboard()


@router.get("/resumen")
async def resumen_periodo(
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...),
    service: ViajeEstadisticasService = Depends(get_service),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener resumen de un período específico"""
    return service.resumen_periodo(fecha_inicio, fecha_fin)
