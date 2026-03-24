from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.infrastructure.database.database import get_db
from app.core.security import verify_token
from app.domain.entities import Usuario
from app.infrastructure.repositories.usuario_repository import UsuarioRepository


# Esquema de seguridad Bearer
security = HTTPBearer()


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Usuario:
    """Obtener usuario actual desde el token JWT"""
    token = credentials.credentials
    user_id = verify_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    usuario_repo = UsuarioRepository(db)
    user = usuario_repo.get_by_id(int(user_id))
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    if user.estado != "ACTIVO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return user


def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Obtener usuario activo actual"""
    if current_user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario eliminado"
        )
    return current_user


def require_roles(allowed_roles: list[str]):
    """Decorador para requerir roles específicos"""
    def role_checker(current_user: Usuario = Depends(get_current_active_user)) -> Usuario:
        user_roles = current_user.roles
        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


def get_current_admin(
    current_user: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """Obtener usuario administrador"""
    if "ADMINISTRADOR" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return current_user


def get_current_operations_user(
    current_user: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """Obtener usuario con permisos de operaciones"""
    allowed_roles = ["ADMINISTRADOR", "OPERACIONES"]
    if not any(role in allowed_roles for role in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de operaciones"
        )
    return current_user


def get_current_finance_user(
    current_user: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """Obtener usuario con permisos financieros"""
    allowed_roles = ["ADMINISTRADOR", "FINANZAS"]
    if not any(role in allowed_roles for role in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos financieros"
        )
    return current_user


def get_current_socio(
    current_user: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """Obtener socio actual"""
    if "SOCIO" not in current_user.roles and "ADMINISTRADOR" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido a socios"
        )
    return current_user


def get_current_chofer(
    current_user: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """Obtener chofer actual"""
    if "CHOFER" not in current_user.roles and "ADMINISTRADOR" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido a choferes"
        )
    return current_user


def check_resource_access(user: Usuario, resource_owner_id: Optional[int] = None) -> bool:
    """Verificar acceso a recurso específico"""
    # Administradores tienen acceso total
    if "ADMINISTRADOR" in user.roles:
        return True
    
    # Si no hay propietario específico, permitir acceso
    if resource_owner_id is None:
        return True
    
    # Socios solo pueden acceder a sus propios recursos
    if "SOCIO" in user.roles:
        # Verificar si el socio es el propietario del recurso
        # Esto requeriría lógica adicional para mapear usuario -> socio
        return True  # Implementar lógica específica
    
    # Choferes solo pueden acceder a sus propios recursos
    if "CHOFER" in user.roles:
        # Verificar si el chofer es el propietario del recurso
        # Esto requeriría lógica adicional para mapear usuario -> chofer
        return True  # Implementar lógica específica
    
    return True


class PermissionChecker:
    """Verificador de permisos granular"""
    
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
    
    def __call__(self, current_user: Usuario = Depends(get_current_active_user)) -> Usuario:
        # Mapa de permisos por rol
        role_permissions = {
            "ADMINISTRADOR": ["*"],  # Acceso total
            "OPERACIONES": ["read:trips", "write:trips", "read:vehicles", "write:vehicles", 
                          "read:drivers", "write:drivers", "read:clients", "write:clients"],
            "FINANZAS": ["read:settlements", "write:settlements", "read:advances", 
                        "write:advances", "read:reports", "export:reports"],
            "SOCIO": ["read:own_vehicles", "read:own_reports", "read:own_trips"],
            "CHOFER": ["read:own_trips", "write:own_expenses"],
            "CLIENTE": ["read:own_orders"]
        }
        
        user_permissions = []
        for role in current_user.roles:
            user_permissions.extend(role_permissions.get(role, []))
        
        # Verificar permiso específico
        if "*" in user_permissions or self.required_permission in user_permissions:
            return current_user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permiso requerido: {self.required_permission}"
        )


# Instancias predefinidas de verificadores de permisos
require_read_trips = PermissionChecker("read:trips")
require_write_trips = PermissionChecker("write:trips")
require_read_reports = PermissionChecker("read:reports")
require_export_reports = PermissionChecker("export:reports")