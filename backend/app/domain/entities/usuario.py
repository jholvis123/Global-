from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.domain.entities.base import BaseModel


class Rol(BaseModel):
    """Modelo de roles del sistema"""
    __tablename__ = "roles"
    
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(200))
    
    # Relaciones
    usuario_roles = relationship("UsuarioRol", back_populates="rol")


class Usuario(BaseModel):
    """Modelo de usuarios del sistema"""
    __tablename__ = "usuarios"
    
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(15))
    estado = Column(String(20), default="ACTIVO", nullable=False)  # ACTIVO, INACTIVO, BLOQUEADO
    intentos_fallidos = Column(Integer, default=0)
    ultimo_login = Column(DateTime)
    
    # Relaciones
    usuario_roles = relationship("UsuarioRol", back_populates="usuario")
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"
    
    @property
    def roles(self):
        """Retorna lista de nombres de roles del usuario"""
        return [ur.rol.nombre for ur in self.usuario_roles if ur.rol]


class UsuarioRol(BaseModel):
    """Modelo de relación usuario-rol"""
    __tablename__ = "usuario_roles"
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    
    # Constraint único para evitar duplicados
    __table_args__ = (UniqueConstraint('usuario_id', 'rol_id', name='_usuario_rol_uc'),)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="usuario_roles")
    rol = relationship("Rol", back_populates="usuario_roles")