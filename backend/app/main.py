from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import uuid
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from sqlmodel import SQLModel
from app.routes import api_router
from app.db.database import engine, Base, get_db
from app.models import *  # Importar todos los modelos para crear tablas
from app.domain.chatbot.entities import ZonaGeografica, Tarifa, SolicitudCotizacion  # Importar entidades del chatbot para crear tablas


# Evento de inicio de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Iniciando Sistema de Gestión de Autotransporte Pesado...")
    print(f"Versión: {settings.APP_VERSION}")
    print(f"Ambiente: {settings.ENVIRONMENT}")
    
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    # Crear tablas del chatbot (SQLModel)
    SQLModel.metadata.create_all(bind=engine)
    
    # Seed data para chatbot
    try:
        seed_chatbot_data()
    except Exception as e:
        print(f"Error en seed (posiblemente tablas no existen): {e}")
    
    yield
    
    # Shutdown
    print(" Cerrando aplicación...")


def seed_chatbot_data():
    """Seed data para el sistema de cotizaciones del chatbot"""
    from sqlalchemy import text
    
    db = next(get_db())
    
    try:
        # Verificar si ya existe data
        result = db.execute(text("SELECT COUNT(*) FROM zonageografica"))
        zonas_count = result.scalar()
        if zonas_count > 0:
            print("Data de chatbot ya existe, saltando seed...")
            return
        
        print("Creando data semilla para chatbot...")
        
        # Crear zonas geográficas de Bolivia usando SQL directo
        zonas_data = [
            ("Santa Cruz", 0.5),
            ("La Paz", 0.6),
            ("Cochabamba", 0.55),
            ("Sucre", 0.58),
            ("Oruro", 0.52),
            ("Potosí", 0.53),
            ("Tarija", 0.51),
            ("Beni", 0.49),
            ("Pando", 0.48),
            ("El Alto", 0.57),
        ]
        
        for nombre, tarifa in zonas_data:
            db.execute(text("INSERT INTO zonageografica (nombre, tarifa_base_km) VALUES (:nombre, :tarifa)"), 
                      {"nombre": nombre, "tarifa": tarifa})
        
        # Crear tarifas entre zonas principales
        rutas_data = [
            ("Santa Cruz", "La Paz", 800, 400),
            ("Santa Cruz", "Cochabamba", 400, 200),
            ("Santa Cruz", "Sucre", 600, 300),
            ("La Paz", "Cochabamba", 200, 100),
            ("La Paz", "Oruro", 250, 125),
            ("Cochabamba", "Sucre", 300, 150),
            ("Cochabamba", "Oruro", 150, 75),
            ("Sucre", "Potosí", 200, 100),
            ("Oruro", "Potosí", 250, 125),
            ("Santa Cruz", "Tarija", 500, 250),
        ]
        
        for origen, destino, distancia, precio in rutas_data:
            # Obtener IDs de zonas
            origen_result = db.execute(text("SELECT id FROM zonageografica WHERE nombre = :nombre"), {"nombre": origen})
            origen_id = origen_result.scalar()
            
            destino_result = db.execute(text("SELECT id FROM zonageografica WHERE nombre = :nombre"), {"nombre": destino})
            destino_id = destino_result.scalar()
            
            if origen_id and destino_id:
                db.execute(text("""
                    INSERT INTO tarifa (zona_origen_id, zona_destino_id, distancia_km, precio_base) 
                    VALUES (:origen_id, :destino_id, :distancia, :precio)
                """), {
                    "origen_id": origen_id,
                    "destino_id": destino_id,
                    "distancia": distancia,
                    "precio": precio
                })
        
        db.commit()
        print("Data semilla para chatbot creada exitosamente!")
        
    except Exception as e:
        print(f"Error creando data semilla: {e}")
        db.rollback()
    finally:
        db.close()


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    Sistema integral de gestión para empresa de autotransporte pesado.
    
    ## Funcionalidades principales:
    
    * **Gestión de Socios**: Registro, contratos, participaciones, anticipos
    * **Gestión de Choferes**: Datos personales, licencias, asignaciones  
    * **Gestión de Vehículos**: Inventario, documentación, mantenimientos
    * **Gestión de Viajes**: Cargas, rutas, tarifas, estados
    * **Gestión Económica**: Liquidaciones, anticipos, saldos
    * **Reportes**: Operativos y financieros con exportación
    * **Seguridad**: Roles, auditoría, multiusuario
    
    ## Localización:
    
    * **Moneda**: Bolivianos (Bs)
    * **Zona horaria**: America/La_Paz  
    * **Idioma**: Español (Bolivia)
    
    ## Autenticación:
    
    Utiliza JWT (JSON Web Tokens) con tokens de acceso y refresh.
    """,
    version=settings.APP_VERSION,
    openapi_url=f"/api/v1/openapi.json" if settings.DEBUG else None,
    docs_url=f"/docs" if settings.DEBUG else None,
    redoc_url=f"/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Registrar manejadores de excepciones globales
register_exception_handlers(app)

# Configurar CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
    )

# Middleware para hosts confiables (solo en producción)
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.transporte.bo", "localhost"]
    )


# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de requests con correlation ID"""
    correlation_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Agregar correlation ID a headers
    request.state.correlation_id = correlation_id
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Log básico (en producción usar logging estructurado)
    print(f"[{correlation_id}] {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    # Agregar headers de respuesta
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Manejadores de excepciones globales
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Manejador personalizado para HTTPException"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "correlation_id": getattr(request.state, "correlation_id", None)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Manejador para excepciones no capturadas"""
    correlation_id = getattr(request.state, "correlation_id", None)
    
    # En producción, loggear el error completo pero no exponerlo
    error_detail = str(exc) if settings.DEBUG else "Error interno del servidor"
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": error_detail,
            "status_code": 500,
            "correlation_id": correlation_id
        }
    )


# Incluir routers de la API
app.include_router(api_router)


# Endpoints de salud y información
@app.get("/", tags=["Sistema"])
async def root():
    """Endpoint raíz con información del sistema"""
    # Debug OpenAI key load
    print(f"DEBUG APP START: OpenAI Key length: {len(settings.OPENAI_API_KEY)}")
    from app.presentation.chatbot.router import servicio_openai
    print(f"DEBUG APP START: servicio_openai.disponible: {servicio_openai.disponible}")
    
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
        "docs": "/docs" if settings.DEBUG else "disabled",
        "api": "/api/v1"
    }


@app.get("/health", tags=["Sistema"])
async def health_check():
    """Health check endpoint para monitoreo"""
    try:
        # Verificar conexión a base de datos
        from app.db.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": time.time(),
            "version": settings.APP_VERSION
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy", 
                "database": "disconnected",
                "error": str(e) if settings.DEBUG else "Database error",
                "timestamp": time.time()
            }
        )


@app.get("/api/v1/info", tags=["Sistema"])
async def api_info():
    """Información de la API"""
    return {
        "api_version": "v1",
        "app_version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timezone": settings.TIMEZONE,
        "locale": settings.LOCALE,
        "currency": settings.CURRENCY,
        "endpoints": {
            "auth": "/api/v1/auth",
            "socios": "/api/v1/socios",
            "choferes": "/api/v1/choferes",
            "clientes": "/api/v1/clientes",
            "vehiculos": "/api/v1/vehiculos", 
            "viajes": "/api/v1/viajes",
            "anticipos": "/api/v1/anticipos",
            "liquidaciones": "/api/v1/liquidaciones",
            "mantenimientos": "/api/v1/mantenimientos",
            "reportes": "/api/v1/reportes"
        }
    }


if __name__ == "__main__":
   
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=settings.DEBUG
    )