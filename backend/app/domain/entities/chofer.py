from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.domain.entities.base import BaseModel


class Chofer(BaseModel):
    """Modelo de choferes"""
    __tablename__ = "choferes"
    
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    ci = Column(String(15), unique=True, nullable=False)
    licencia_numero = Column(String(20), nullable=False)
    licencia_categoria = Column(String(10), nullable=False)
    licencia_vencimiento = Column(Date, nullable=False)
    telefono = Column(String(15))
    direccion = Column(String(200))
    experiencia_anos = Column(Integer, default=0)
    estado = Column(String(20), default="ACTIVO", nullable=False)  # ACTIVO, INACTIVO, SUSPENDIDO
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="choferes")
    viajes = relationship("Viaje", back_populates="chofer")
    anticipos = relationship("Anticipo", back_populates="chofer")
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del chofer"""
        return f"{self.nombre} {self.apellido}"
    
    @property
    def licencia_vigente(self):
        """Indica si la licencia está vigente"""
        return self.licencia_vencimiento >= date.today()
    
    @property
    def dias_para_vencer_licencia(self):
        """Días restantes para que venza la licencia"""
        if self.licencia_vigente:
            return (self.licencia_vencimiento - date.today()).days
        return 0
    
    @property
    def licencia_pronta_vencer(self):
        """Indica si la licencia vence en los próximos 30 días"""
        return 0 <= self.dias_para_vencer_licencia <= 30