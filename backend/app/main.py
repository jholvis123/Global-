import time
import uuid
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlmodel import SQLModel

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.api.v1.endpoints import api_router
from sqlalchemy import text
from app.infrastructure.database.database import engine, Base
from app.infrastructure.database.seeds import crear_datos_semilla_chatbot
from app.domain.entities import *  # Importar para creación de tablas

# Configuración de logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Iniciando Sistema de Gestión de Autotransporte Pesado...")
    logger.info(f"Versión: {settings.APP_VERSION} | Ambiente: {settings.ENVIRONMENT}")
    
    # Crear tablas (SQLAlchemy & SQLModel)
    Base.metadata.create_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
    
    # Ejecutar datos semilla
    try:
        crear_datos_semilla_chatbot()
    except Exception as e:
        logger.error(f"Error al ejecutar datos semilla: {e}")
    
    yield
    
    # Shutdown
    logger.info("Cerrando aplicación...")


app = FastAPI(
    title=settings.APP_NAME,
    description="""
    Sistema integral de gestión para empresa de autotransporte pesado.
    Localización: Bolivia (Bs, America/La_Paz).
    """,
    version=settings.APP_VERSION,
    openapi_url=f"/api/v1/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Registrar manejadores de excepciones globales (Centralizado en core)
register_exception_handlers(app)

# Middlewares
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    correlation_id = str(uuid.uuid4())
    start_time = time.time()
    request.state.correlation_id = correlation_id
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"[{correlation_id}] {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Router Principal
app.include_router(api_router)

# Endpoints de sistema
@app.get("/", tags=["Sistema"])
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }

@app.get("/health", tags=["Sistema"])
async def health_check():
    try:
        from app.infrastructure.database.database import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check fallido: {e}")
        return {"status": "unhealthy", "database": "disconnected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
