from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Cliente(BaseModel):
    """Modelo de clientes"""
    __tablename__ = "clientes"
    
    razon_social = Column(String(150), nullable=False)
    nit = Column(String(20), unique=True)
    contacto_nombre = Column(String(100))
    contacto_telefono = Column(String(15))
    contacto_email = Column(String(100))
    direccion = Column(String(200))
    estado = Column(String(20), default="ACTIVO", nullable=False)  # ACTIVO, INACTIVO
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="clientes")
    viajes = relationship("Viaje", back_populates="cliente")
    
    @property
    def contacto_principal(self):
        """Retorna el contacto principal (teléfono o email)"""
        return self.contacto_telefono if self.contacto_telefono else self.contacto_email