from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.domain.entities.base import BaseModel


class Anticipo(BaseModel):
    """Modelo de anticipos"""
    __tablename__ = "anticipos"
    
    viaje_id = Column(Integer, ForeignKey("viajes.id"), nullable=True)
    socio_id = Column(Integer, ForeignKey("socios.id"), nullable=True)
    chofer_id = Column(Integer, ForeignKey("choferes.id"), nullable=True)
    beneficiario_tipo = Column(String(10), nullable=False)  # SOCIO, CHOFER
    monto_bs = Column(Numeric(10, 2), nullable=False)
    fecha = Column(DateTime, nullable=False, index=True)
    observacion = Column(String(300))
    estado = Column(String(20), default="PENDIENTE", nullable=False)  # PENDIENTE, LIQUIDADO
    
    # Constraints
    __table_args__ = (
        CheckConstraint("beneficiario_tipo IN ('SOCIO', 'CHOFER')", name="ck_anticipo_beneficiario_tipo"),
        CheckConstraint("estado IN ('PENDIENTE', 'LIQUIDADO')", name="ck_anticipo_estado"),
    )
    
    # Relaciones
    viaje = relationship("Viaje", back_populates="anticipos")
    socio = relationship("Socio", back_populates="anticipos")
    chofer = relationship("Chofer", back_populates="anticipos")
    
    @property
    def beneficiario_nombre(self):
        """Retorna el nombre del beneficiario"""
        if self.beneficiario_tipo == "SOCIO" and self.socio:
            return self.socio.nombre
        elif self.beneficiario_tipo == "CHOFER" and self.chofer:
            return self.chofer.nombre_completo
        return "Sin beneficiario"
    
    @property
    def monto_formateado(self):
        """Retorna el monto formateado en bolivianos"""
        return f"Bs {self.monto_bs:,.2f}"
    
    @property
    def es_para_viaje_especifico(self):
        """Indica si el anticipo es para un viaje específico"""
        return bool(self.viaje_id)