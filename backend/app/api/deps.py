"""
Dependencias de FastAPI para inyección en rutas.
"""
from typing import Generator
from functools import lru_cache
from fastapi import Depends

from app.infrastructure.database.database import SessionLocal, get_db
from app.core.unit_of_work import UnitOfWork, UnitOfWorkFactory
from app.core.deps import get_current_user, get_current_active_user, get_current_admin


# ==================== Unit of Work ====================

@lru_cache()
def get_uow_factory() -> UnitOfWorkFactory:
    """Obtener factory de Unit of Work (singleton)"""
    return UnitOfWorkFactory(SessionLocal)


def get_uow(factory: UnitOfWorkFactory = Depends(get_uow_factory)) -> UnitOfWork:
    """
    Obtener instancia de Unit of Work para usar en rutas.
    
    Uso en rutas:
    ```python
    @router.get("/viajes")
    async def listar_viajes(uow: UnitOfWork = Depends(get_uow)):
        service = ViajeService(uow)
        return service.listar_viajes()
    ```
    """
    return factory.create()


# ==================== Services ====================

def get_viaje_service(uow: UnitOfWork = Depends(get_uow)):
    """Obtener servicio de viajes"""
    from app.application.services.viaje_service import ViajeService
    return ViajeService(uow)


def get_liquidacion_service(uow: UnitOfWork = Depends(get_uow)):
    """Obtener servicio de liquidaciones"""
    from app.application.services.viaje_service import LiquidacionService
    return LiquidacionService(uow)


def get_reporte_service(uow: UnitOfWork = Depends(get_uow)):
    """Obtener servicio de reportes"""
    from app.application.services.viaje_service import ReporteService
    return ReporteService(uow)


# ==================== Re-exportar dependencias existentes ====================

__all__ = [
    # Unit of Work
    "get_uow",
    "get_uow_factory",
    
    # Services
    "get_viaje_service",
    "get_liquidacion_service",
    "get_reporte_service",
    
    # Auth (re-exported)
    "get_current_user",
    "get_current_active_user",
    "get_current_admin",
]
