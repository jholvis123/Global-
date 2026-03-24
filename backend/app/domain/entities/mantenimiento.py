from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import date
from app.domain.entities.base import BaseModel


class Mantenimiento(BaseModel):
    """Modelo de mantenimientos de vehículos"""
    __tablename__ = "mantenimientos"
    
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False, index=True)
    tipo = Column(String(20), nullable=False)  # PREVENTIVO, CORRECTIVO
    descripcion = Column(String(300), nullable=False)
    costo_bs = Column(Numeric(10, 2), nullable=False)
    fecha = Column(DateTime, nullable=False, index=True)
    taller = Column(String(100))
    proximo_km = Column(Integer)
    proxima_fecha = Column(Date)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("tipo IN ('PREVENTIVO', 'CORRECTIVO')", name="ck_mantenimiento_tipo"),
    )
    
    # Relaciones
    vehiculo = relationship("Vehiculo", back_populates="mantenimientos")
    
    @property
    def costo_formateado(self):
        """Retorna el costo formateado en bolivianos"""
        return f"Bs {self.costo_bs:,.2f}"
    
    @property
    def es_preventivo(self):
        """Indica si es un mantenimiento preventivo"""
        return self.tipo == "PREVENTIVO"
    
    @property
    def es_correctivo(self):
        """Indica si es un mantenimiento correctivo"""
        return self.tipo == "CORRECTIVO"
    
    @property
    def tiene_programacion_siguiente(self):
        """Indica si tiene programado el próximo mantenimiento"""
        return bool(self.proximo_km or self.proxima_fecha)
    
    @property
    def dias_hasta_proximo(self):
        """Días hasta el próximo mantenimiento programado"""
        if self.proxima_fecha:
            return (self.proxima_fecha - date.today()).days
        return None
    
    @property
    def mantenimiento_proximo(self):
        """Indica si el próximo mantenimiento está próximo (30 días)"""
        if self.dias_hasta_proximo is not None:
            return 0 <= self.dias_hasta_proximo <= 30
        return False