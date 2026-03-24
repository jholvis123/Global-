"""
Routes - API Router Principal
"""
from fastapi import APIRouter

from .auth import router as auth_router
from .socios import router as socios_router
from .vehiculos import router as vehiculos_router
from .choferes import router as choferes_router
from .clientes import router as clientes_router
from .viajes import router as viajes_router
from .anticipos import router as anticipos_router
from .liquidaciones import router as liquidaciones_router
from .mantenimientos import router as mantenimientos_router
from .dashboard import router as dashboard_router
from app.api.v1.endpoints.chatbot.router import router as chatbot_router

# Router principal de la API
api_router = APIRouter(prefix="/api/v1")

# Registrar todos los routers (ya tienen sus prefijos internos)
api_router.include_router(auth_router)
api_router.include_router(socios_router)
api_router.include_router(vehiculos_router)
api_router.include_router(choferes_router)
api_router.include_router(clientes_router)
api_router.include_router(viajes_router)
api_router.include_router(anticipos_router)
api_router.include_router(liquidaciones_router)
api_router.include_router(mantenimientos_router)
api_router.include_router(dashboard_router)
api_router.include_router(chatbot_router)

__all__ = ["api_router"]