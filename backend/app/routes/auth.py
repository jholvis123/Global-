from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.deps import get_current_active_user, get_current_admin
from app.controllers.auth_controller import AuthController
from app.schemas.usuario import (
    LoginRequest, 
    TokenResponse, 
    UsuarioCreate, 
    UsuarioResponse, 
    ChangePasswordRequest
)
from app.models import Usuario


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión")
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Autenticar usuario y obtener tokens de acceso.
    
    - **email**: Email del usuario
    - **password**: Contraseña del usuario
    
    Retorna tokens de acceso y refresh junto con información del usuario.
    """
    controller = AuthController(db)
    return controller.login(login_data)


@router.post("/refresh", response_model=TokenResponse, summary="Refrescar token")
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refrescar token de acceso usando el refresh token.
    
    - **refresh_token**: Token de refresh válido
    
    Retorna un nuevo token de acceso.
    """
    controller = AuthController(db)
    return controller.refresh_token(refresh_token)


@router.post("/register", response_model=UsuarioResponse, summary="Registrar usuario")
async def register(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """
    Registrar nuevo usuario en el sistema.
    
    **Requiere permisos de administrador.**
    
    - **email**: Email único del usuario
    - **password**: Contraseña (mínimo 8 caracteres)
    - **nombre**: Nombre del usuario
    - **apellido**: Apellido del usuario
    - **roles**: Lista de roles a asignar
    """
    controller = AuthController(db)
    return controller.register(usuario_data, current_user)


@router.post("/change-password", summary="Cambiar contraseña")
async def change_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Cambiar contraseña del usuario actual.
    
    - **password_actual**: Contraseña actual del usuario
    - **password_nueva**: Nueva contraseña (mínimo 8 caracteres)
    """
    controller = AuthController(db)
    success = controller.change_password(password_data, current_user)
    
    if success:
        return {"message": "Contraseña actualizada exitosamente"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar contraseña"
        )


@router.post("/logout", summary="Cerrar sesión")
async def logout(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Cerrar sesión del usuario actual.
    
    En una implementación completa, esto invalidaría el token.
    """
    controller = AuthController(db)
    return controller.logout(current_user)


@router.get("/profile", response_model=UsuarioResponse, summary="Obtener perfil")
async def get_profile(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtener información del perfil del usuario actual.
    
    Incluye roles asignados y estadísticas básicas.
    """
    controller = AuthController(db)
    return controller.get_profile(current_user)


@router.post("/unblock/{user_id}", summary="Desbloquear usuario")
async def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """
    Desbloquear usuario que fue bloqueado por intentos fallidos.
    
    **Requiere permisos de administrador.**
    
    - **user_id**: ID del usuario a desbloquear
    """
    controller = AuthController(db)
    success = controller.unblock_user(user_id, current_user)
    
    if success:
        return {"message": f"Usuario {user_id} desbloqueado exitosamente"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al desbloquear usuario"
        )


@router.get("/me", response_model=UsuarioResponse, summary="Mi información")
async def get_me(
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtener información básica del usuario actual.
    
    Endpoint alternativo más simple que /profile.
    """
    return current_user