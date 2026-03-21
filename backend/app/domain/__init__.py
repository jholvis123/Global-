"""
Domain Layer - __init__.py
Expone las clases principales del dominio.
"""
from app.domain.exceptions import (
    DomainException,
    BusinessRuleException,
    EntityNotFoundException,
    DuplicateEntityException,
    InvalidStateTransitionException,
    ResourceNotAvailableException,
    ValidationException,
    UnauthorizedException,
    InsufficientFundsException,
    QuotaExceededException
)

from app.domain.value_objects import (
    Dinero,
    Ruta,
    Tarifa,
    Periodo,
    Porcentaje
)

from app.domain.services import (
    CalculadoraTarifa,
    CalculadoraLiquidacion,
    ValidadorViaje,
    CalculadoraEstadisticas
)


__all__ = [
    # Exceptions
    "DomainException",
    "BusinessRuleException",
    "EntityNotFoundException",
    "DuplicateEntityException",
    "InvalidStateTransitionException",
    "ResourceNotAvailableException",
    "ValidationException",
    "UnauthorizedException",
    "InsufficientFundsException",
    "QuotaExceededException",
    
    # Value Objects
    "Dinero",
    "Ruta",
    "Tarifa",
    "Periodo",
    "Porcentaje",
    
    # Domain Services
    "CalculadoraTarifa",
    "CalculadoraLiquidacion",
    "ValidadorViaje",
    "CalculadoraEstadisticas",
]
