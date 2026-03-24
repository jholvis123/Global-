"""
Manejador global de excepciones para FastAPI.
Convierte excepciones de dominio a respuestas HTTP apropiadas.
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Union
import traceback
import logging

from app.domain.exceptions import (
    DomainException,
    EntityNotFoundException,
    BusinessRuleException,
    ValidationException,
    InvalidStateTransitionException,
    ResourceNotAvailableException,
    UnauthorizedException,
    DuplicateEntityException,
    InsufficientFundsException
)
from app.api.schemas.responses import ErrorResponse, ErrorDetail


logger = logging.getLogger(__name__)


def create_error_response(
    error: str,
    code: str,
    status_code: int,
    details: list = None,
    path: str = None
) -> JSONResponse:
    """Crear respuesta de error estandarizada"""
    response = ErrorResponse(
        error=error,
        code=code,
        details=details,
        path=path
    )
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump()
    )


async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    """Manejar excepciones de dominio"""
    
    # Mapear tipo de excepción a código HTTP
    status_code_map = {
        EntityNotFoundException: 404,
        DuplicateEntityException: 409,
        ValidationException: 422,
        BusinessRuleException: 400,
        InvalidStateTransitionException: 400,
        ResourceNotAvailableException: 409,
        UnauthorizedException: 403,
        InsufficientFundsException: 400,
    }
    
    status_code = status_code_map.get(type(exc), 400)
    
    details = None
    if exc.details:
        details = [ErrorDetail(
            field=exc.details.get("field"),
            message=exc.message,
            code=exc.code
        )]
    
    logger.warning(f"Domain Exception: {exc.code} - {exc.message}")
    
    return create_error_response(
        error=exc.message,
        code=exc.code,
        status_code=status_code,
        details=details,
        path=str(request.url.path)
    )


async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
) -> JSONResponse:
    """Manejar errores de validación de Pydantic"""
    
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        details.append(ErrorDetail(
            field=field,
            message=error["msg"],
            code=error.get("type", "validation_error")
        ))
    
    logger.warning(f"Validation Error: {len(details)} errores en {request.url.path}")
    
    return create_error_response(
        error="Error de validación en los datos enviados",
        code="VALIDATION_ERROR",
        status_code=422,
        details=details,
        path=str(request.url.path)
    )


async def http_exception_handler(
    request: Request, 
    exc: Union[HTTPException, StarletteHTTPException]
) -> JSONResponse:
    """Manejar excepciones HTTP estándar"""
    
    code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        422: "UNPROCESSABLE_ENTITY",
        429: "TOO_MANY_REQUESTS",
        500: "INTERNAL_ERROR",
    }
    
    return create_error_response(
        error=str(exc.detail) if hasattr(exc, 'detail') else "Error HTTP",
        code=code_map.get(exc.status_code, "HTTP_ERROR"),
        status_code=exc.status_code,
        path=str(request.url.path)
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Manejar excepciones no capturadas"""
    
    # Log completo del error
    logger.error(f"Unhandled Exception: {type(exc).__name__} - {str(exc)}")
    logger.error(traceback.format_exc())
    
    # En producción, no revelar detalles internos
    return create_error_response(
        error="Ha ocurrido un error interno. Por favor, intente nuevamente.",
        code="INTERNAL_ERROR",
        status_code=500,
        path=str(request.url.path)
    )


def register_exception_handlers(app):
    """Registrar todos los manejadores de excepciones en la app FastAPI"""
    
    # Excepciones de dominio
    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(EntityNotFoundException, domain_exception_handler)
    app.add_exception_handler(BusinessRuleException, domain_exception_handler)
    app.add_exception_handler(ValidationException, domain_exception_handler)
    app.add_exception_handler(InvalidStateTransitionException, domain_exception_handler)
    app.add_exception_handler(ResourceNotAvailableException, domain_exception_handler)
    app.add_exception_handler(UnauthorizedException, domain_exception_handler)
    app.add_exception_handler(DuplicateEntityException, domain_exception_handler)
    app.add_exception_handler(InsufficientFundsException, domain_exception_handler)
    
    # Excepciones de validación
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    
    # Excepciones HTTP
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    
    # Excepción genérica (catch-all)
    app.add_exception_handler(Exception, generic_exception_handler)
    
    logger.info("Exception handlers registered successfully")
