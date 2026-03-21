from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import (
    create_access_token, 
    create_refresh_token, 
    verify_refresh_token,
    validate_password_strength
)
from app.core.config import settings
from app.schemas.usuario import LoginRequest, TokenResponse, UsuarioCreate, ChangePasswordRequest
from app.repositories.usuario_repository import UsuarioRepository
from app.models import Usuario


class AuthController:
    """Controlador para autenticación"""
    
    def __init__(self, db: Session):
        self.db = db
        self.usuario_repo = UsuarioRepository(db)
    
    def login(self, login_data: LoginRequest) -> TokenResponse:
        """Autenticar usuario y generar tokens"""
        # Autenticar usuario
        usuario = self.usuario_repo.authenticate(login_data.email, login_data.password)
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )
        
        if usuario.estado == "BLOQUEADO":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario bloqueado por múltiples intentos fallidos"
            )
        
        if usuario.estado != "ACTIVO":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        # Actualizar último login
        usuario.ultimo_login = datetime.utcnow()
        self.db.commit()
        
        # Generar tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        access_token = create_access_token(
            subject=usuario.id, 
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            subject=usuario.id,
            expires_delta=refresh_token_expires
        )
        
        # Obtener usuario con roles para la respuesta
        usuario_con_roles = self.usuario_repo.get_with_roles(usuario.id)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            usuario=usuario_con_roles
        )
    
    def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Refrescar token de acceso"""
        user_id = verify_refresh_token(refresh_token)
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de refresh inválido o expirado"
            )
        
        usuario = self.usuario_repo.get_with_roles(int(user_id))
        
        if not usuario or usuario.estado != "ACTIVO":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado o inactivo"
            )
        
        # Generar nuevo access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            subject=usuario.id,
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=refresh_token,  # El refresh token sigue siendo válido
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            usuario=usuario
        )
    
    def register(self, usuario_data: UsuarioCreate, current_user: Usuario) -> Usuario:
        """Registrar nuevo usuario (solo administradores)"""
        # Verificar que el usuario actual es administrador
        if "ADMINISTRADOR" not in current_user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo administradores pueden registrar usuarios"
            )
        
        # Verificar que el email no esté en uso
        if self.usuario_repo.get_by_email(usuario_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Validar fortaleza de contraseña
        is_valid, message = validate_password_strength(usuario_data.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Crear usuario
        usuario_dict = usuario_data.dict(exclude={"password"})
        usuario = self.usuario_repo.create_with_password(
            usuario_dict, 
            usuario_data.password
        )
        
        return usuario
    
    def change_password(
        self, 
        password_data: ChangePasswordRequest, 
        current_user: Usuario
    ) -> bool:
        """Cambiar contraseña del usuario actual"""
        # Verificar contraseña actual
        usuario = self.usuario_repo.authenticate(
            current_user.email, 
            password_data.password_actual
        )
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta"
            )
        
        # Validar nueva contraseña
        is_valid, message = validate_password_strength(password_data.password_nueva)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Actualizar contraseña
        success = self.usuario_repo.update_password(
            current_user.id, 
            password_data.password_nueva
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la contraseña"
            )
        
        return True
    
    def logout(self, current_user: Usuario) -> dict:
        """Cerrar sesión (en una implementación completa se invalidaría el token)"""
        # En una implementación completa, aquí se invalidaría el token
        # agregándolo a una lista negra o usando un sistema de revocación
        return {"message": "Sesión cerrada exitosamente"}
    
    def get_profile(self, current_user: Usuario) -> Usuario:
        """Obtener perfil del usuario actual"""
        return self.usuario_repo.get_with_roles(current_user.id)
    
    def unblock_user(self, user_id: int, current_user: Usuario) -> bool:
        """Desbloquear usuario (solo administradores)"""
        if "ADMINISTRADOR" not in current_user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo administradores pueden desbloquear usuarios"
            )
        
        success = self.usuario_repo.unblock_user(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return True