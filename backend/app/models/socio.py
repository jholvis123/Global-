from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Socio(BaseModel):
    """Modelo de socios"""
    __tablename__ = "socios"
    
    nombre = Column(String(100), nullable=False)
    nit = Column(String(20), unique=True)
    ci = Column(String(15))
    direccion = Column(String(200))
    telefono = Column(String(15))
    email = Column(String(100))
    cuenta_bancaria = Column(String(50))
    banco = Column(String(50))
    participacion_tipo = Column(String(10), default="NETO", nullable=False)  # NETO, BRUTO
    participacion_valor = Column(Numeric(5, 2), nullable=False)  # Porcentaje o monto fijo
    saldo_anticipos = Column(Numeric(12, 2), default=0.00)
    estado = Column(String(20), default="ACTIVO", nullable=False)  # ACTIVO, INACTIVO
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="socios")
    vehiculos = relationship("Vehiculo", back_populates="socio")
    anticipos = relationship("Anticipo", back_populates="socio")
    
    @property
    def es_persona_natural(self):
        """Indica si es persona natural (tiene CI)"""
        return bool(self.ci)
    
    @property
    def identificacion_principal(self):
        """Retorna la identificación principal (CI o NIT)"""
        return self.ci if self.ci else self.nit