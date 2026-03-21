from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models import Usuario, Rol, UsuarioRol
from app.repositories.base_repository import BaseRepository
from app.core.security import get_password_hash, verify_password


class UsuarioRepository(BaseRepository[Usuario]):
    """Repositorio para gestión de usuarios"""
    
    def __init__(self, db: Session):
        super().__init__(db, Usuario)
    
    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        return self.db.query(Usuario).filter(
            and_(
                Usuario.email == email,
                Usuario.deleted_at.is_(None)
            )
        ).first()
    
    def create_with_password(self, usuario_data: dict, password: str) -> Usuario:
        """Crear usuario con contraseña hasheada"""
        usuario_data['password_hash'] = get_password_hash(password)
        roles = usuario_data.pop('roles', [])
        
        # Crear usuario
        usuario = self.create(usuario_data)
        
        # Asignar roles
        if roles:
            self.assign_roles(usuario.id, roles)
        
        return usuario
    
    def authenticate(self, email: str, password: str) -> Optional[Usuario]:
        """Autenticar usuario"""
        usuario = self.get_by_email(email)
        if not usuario:
            return None
        
        if not verify_password(password, usuario.password_hash):
            # Incrementar intentos fallidos
            usuario.intentos_fallidos += 1
            if usuario.intentos_fallidos >= 5:
                usuario.estado = "BLOQUEADO"
            self.db.commit()
            return None
        
        # Reset intentos fallidos en login exitoso
        if usuario.intentos_fallidos > 0:
            usuario.intentos_fallidos = 0
            self.db.commit()
        
        return usuario
    
    def update_password(self, user_id: int, new_password: str) -> bool:
        """Actualizar contraseña del usuario"""
        usuario = self.get_by_id(user_id)
        if not usuario:
            return False
        
        usuario.password_hash = get_password_hash(new_password)
        self.db.commit()
        return True
    
    def get_with_roles(self, user_id: int) -> Optional[Usuario]:
        """Obtener usuario con sus roles cargados"""
        return self.db.query(Usuario).options(
            joinedload(Usuario.usuario_roles).joinedload(UsuarioRol.rol)
        ).filter(
            and_(
                Usuario.id == user_id,
                Usuario.deleted_at.is_(None)
            )
        ).first()
    
    def assign_roles(self, user_id: int, role_names: List[str]) -> bool:
        """Asignar roles a usuario"""
        usuario = self.get_by_id(user_id)
        if not usuario:
            return False
        
        # Obtener roles por nombres
        roles = self.db.query(Rol).filter(Rol.nombre.in_(role_names)).all()
        if len(roles) != len(role_names):
            return False
        
        # Eliminar roles existentes
        self.db.query(UsuarioRol).filter(
            UsuarioRol.usuario_id == user_id
        ).delete()
        
        # Asignar nuevos roles
        for rol in roles:
            usuario_rol = UsuarioRol(usuario_id=user_id, rol_id=rol.id)
            self.db.add(usuario_rol)
        
        self.db.commit()
        return True
    
    def remove_roles(self, user_id: int, role_names: List[str]) -> bool:
        """Remover roles específicos de usuario"""
        roles = self.db.query(Rol).filter(Rol.nombre.in_(role_names)).all()
        role_ids = [rol.id for rol in roles]
        
        self.db.query(UsuarioRol).filter(
            and_(
                UsuarioRol.usuario_id == user_id,
                UsuarioRol.rol_id.in_(role_ids)
            )
        ).delete()
        
        self.db.commit()
        return True
    
    def get_by_role(self, role_name: str) -> List[Usuario]:
        """Obtener usuarios por rol"""
        return self.db.query(Usuario).join(UsuarioRol).join(Rol).filter(
            and_(
                Rol.nombre == role_name,
                Usuario.deleted_at.is_(None)
            )
        ).all()
    
    def block_user(self, user_id: int) -> bool:
        """Bloquear usuario"""
        return self.update(user_id, {'estado': 'BLOQUEADO'}) is not None
    
    def unblock_user(self, user_id: int) -> bool:
        """Desbloquear usuario"""
        usuario = self.get_by_id(user_id)
        if not usuario:
            return False
        
        usuario.estado = 'ACTIVO'
        usuario.intentos_fallidos = 0
        self.db.commit()
        return True
    
    def get_active_users(self) -> List[Usuario]:
        """Obtener usuarios activos"""
        return self.db.query(Usuario).filter(
            and_(
                Usuario.estado == "ACTIVO",
                Usuario.deleted_at.is_(None)
            )
        ).all()
    
    def search_users(self, search_term: str) -> List[Usuario]:
        """Buscar usuarios por nombre, apellido o email"""
        return self.search(search_term, ['nombre', 'apellido', 'email'])


class RolRepository(BaseRepository[Rol]):
    """Repositorio para gestión de roles"""
    
    def __init__(self, db: Session):
        super().__init__(db, Rol)
    
    def get_by_name(self, name: str) -> Optional[Rol]:
        """Obtener rol por nombre"""
        return self.get_by_field('nombre', name)
    
    def get_all_roles(self) -> List[Rol]:
        """Obtener todos los roles disponibles"""
        return self.get_all()