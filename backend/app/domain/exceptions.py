"""
Excepciones de dominio - Errores de negocio claros y específicos
"""
from typing import Optional, Dict, Any


class DomainException(Exception):
    """Excepción base de dominio"""
    
    def __init__(
        self, 
        message: str, 
        code: str = "DOMAIN_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class BusinessRuleException(DomainException):
    """Violación de regla de negocio"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "BUSINESS_RULE_VIOLATION", details)


class EntityNotFoundException(DomainException):
    """Entidad no encontrada"""
    
    def __init__(self, entity: str, entity_id: Any):
        super().__init__(
            f"{entity} con ID {entity_id} no encontrado",
            "ENTITY_NOT_FOUND",
            {"entity": entity, "id": entity_id}
        )


class DuplicateEntityException(DomainException):
    """Entidad duplicada"""
    
    def __init__(self, entity: str, field: str, value: Any):
        super().__init__(
            f"Ya existe un {entity} con {field} = {value}",
            "DUPLICATE_ENTITY",
            {"entity": entity, "field": field, "value": value}
        )


class InvalidStateTransitionException(DomainException):
    """Transición de estado inválida"""
    
    def __init__(self, entity: str, current_state: str, target_state: str):
        super().__init__(
            f"No se puede cambiar {entity} de '{current_state}' a '{target_state}'",
            "INVALID_STATE_TRANSITION",
            {
                "entity": entity,
                "current_state": current_state,
                "target_state": target_state
            }
        )


class InsufficientFundsException(DomainException):
    """Fondos insuficientes"""
    
    def __init__(self, required: float, available: float):
        super().__init__(
            f"Fondos insuficientes. Requerido: Bs {required:.2f}, Disponible: Bs {available:.2f}",
            "INSUFFICIENT_FUNDS",
            {"required": required, "available": available}
        )


class ResourceNotAvailableException(DomainException):
    """Recurso no disponible"""
    
    def __init__(self, resource: str, resource_id: Any, reason: str = None):
        message = f"{resource} con ID {resource_id} no está disponible"
        if reason:
            message += f": {reason}"
        super().__init__(
            message,
            "RESOURCE_NOT_AVAILABLE",
            {"resource": resource, "id": resource_id, "reason": reason}
        )


class ValidationException(DomainException):
    """Error de validación"""
    
    def __init__(self, field: str, message: str):
        super().__init__(
            f"Error de validación en '{field}': {message}",
            "VALIDATION_ERROR",
            {"field": field}
        )


class UnauthorizedException(DomainException):
    """No autorizado"""
    
    def __init__(self, action: str, resource: str = None):
        message = f"No tiene permisos para {action}"
        if resource:
            message += f" en {resource}"
        super().__init__(message, "UNAUTHORIZED", {"action": action, "resource": resource})


class QuotaExceededException(DomainException):
    """Cuota excedida"""
    
    def __init__(self, resource: str, limit: int, current: int):
        super().__init__(
            f"Cuota de {resource} excedida. Límite: {limit}, Actual: {current}",
            "QUOTA_EXCEEDED",
            {"resource": resource, "limit": limit, "current": current}
        )
