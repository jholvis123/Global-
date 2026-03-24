from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.domain.entities.base import BaseModel


class Liquidacion(BaseModel):
    """Modelo de liquidaciones de viajes"""
    __tablename__ = "liquidaciones"
    
    viaje_id = Column(Integer, ForeignKey("viajes.id"), unique=True, nullable=False)
    ingreso_bs = Column(Numeric(12, 2), nullable=False)
    gastos_bs = Column(Numeric(12, 2), nullable=False)
    pago_socio_bs = Column(Numeric(12, 2), nullable=False)
    saldo_socio_bs = Column(Numeric(12, 2), nullable=False)
    saldo_chofer_bs = Column(Numeric(12, 2), default=0.00)
    fecha = Column(DateTime, nullable=False, index=True)
    
    # Relaciones
    viaje = relationship("Viaje", back_populates="liquidacion")
    
    @property
    def margen_bs(self):
        """Margen bruto del viaje (ingreso - gastos)"""
        return float(self.ingreso_bs - self.gastos_bs)
    
    @property
    def ingreso_formateado(self):
        """Retorna el ingreso formateado"""
        return f"Bs {self.ingreso_bs:,.2f}"
    
    @property
    def gastos_formateados(self):
        """Retorna los gastos formateados"""
        return f"Bs {self.gastos_bs:,.2f}"
    
    @property
    def margen_formateado(self):
        """Retorna el margen formateado"""
        return f"Bs {self.margen_bs:,.2f}"
    
    @property
    def pago_socio_formateado(self):
        """Retorna el pago al socio formateado"""
        return f"Bs {self.pago_socio_bs:,.2f}"
    
    @property
    def saldo_socio_formateado(self):
        """Retorna el saldo del socio formateado"""
        signo = "+" if self.saldo_socio_bs >= 0 else "-"
        return f"{signo} Bs {abs(self.saldo_socio_bs):,.2f}"
    
    @property
    def rentabilidad_porcentaje(self):
        """Calcula el porcentaje de rentabilidad"""
        if self.ingreso_bs > 0:
            return (self.margen_bs / float(self.ingreso_bs)) * 100
        return 0.0