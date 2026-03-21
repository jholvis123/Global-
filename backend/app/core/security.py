from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
import secrets


# Contexto para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """Crear token de acceso JWT"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """Crear token de refresh JWT"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """Verificar y decodificar token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None


def verify_refresh_token(token: str) -> Optional[str]:
    """Verificar token de refresh"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "refresh":
            return None
        return user_id
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generar hash de contraseña"""
    return pwd_context.hash(password)


def generate_password_reset_token() -> str:
    """Generar token para reseteo de contraseña"""
    return secrets.token_urlsafe(32)


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validar fortaleza de contraseña"""
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not any(c.islower() for c in password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    if not any(c.isupper() for c in password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    if not any(c.isdigit() for c in password):
        return False, "La contraseña debe contener al menos un número"
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, "La contraseña debe contener al menos un carácter especial"
    
    return True, "Contraseña válida"


class RoleChecker:
    """Verificador de roles"""
    
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, user_roles: list[str]) -> bool:
        """Verificar si el usuario tiene alguno de los roles permitidos"""
        return any(role in self.allowed_roles for role in user_roles)


# Instancias predefinidas de verificadores de roles
require_admin = RoleChecker(["ADMINISTRADOR"])
require_operations = RoleChecker(["ADMINISTRADOR", "OPERACIONES"])
require_finance = RoleChecker(["ADMINISTRADOR", "FINANZAS"])
require_partner = RoleChecker(["ADMINISTRADOR", "SOCIO"])
require_driver = RoleChecker(["ADMINISTRADOR", "CHOFER"])
require_client = RoleChecker(["ADMINISTRADOR", "CLIENTE"])
require_any_authenticated = RoleChecker([
    "ADMINISTRADOR", "OPERACIONES", "FINANZAS", "SOCIO", "CHOFER", "CLIENTE"
])