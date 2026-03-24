from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import case, text
from app.domain.entities.base import BaseModel


class Viaje(BaseModel):
    """Modelo de viajes"""
    __tablename__ = "viajes"
    
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False, index=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False, index=True)
    chofer_id = Column(Integer, ForeignKey("choferes.id"), nullable=False, index=True)
    origen = Column(String(100), nullable=False)
    destino = Column(String(100), nullable=False)
    fecha_salida = Column(DateTime, nullable=False, index=True)
    fecha_llegada = Column(DateTime)
    tipo_carga = Column(String(50), nullable=False, index=True)
    peso_ton = Column(Numeric(8, 2), nullable=False)
    volumen_m3 = Column(Numeric(8, 2))
    km_estimado = Column(Integer, nullable=False)
    km_real = Column(Integer)
    tarifa_tipo = Column(String(10), nullable=False)  # KM, TON, FIJA
    tarifa_valor = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(20), default="PLANIFICADO", nullable=False, index=True)  # PLANIFICADO, EN_RUTA, ENTREGADO, LIQUIDADO
    notas = Column(String(500))
    
    # Constraints
    __table_args__ = (
        CheckConstraint("tarifa_tipo IN ('KM', 'TON', 'FIJA')", name="ck_viaje_tarifa_tipo"),
        CheckConstraint("estado IN ('PLANIFICADO', 'EN_RUTA', 'ENTREGADO', 'LIQUIDADO')", name="ck_viaje_estado"),
    )
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="viajes")
    vehiculo = relationship("Vehiculo", back_populates="viajes")
    chofer = relationship("Chofer", back_populates="viajes")
    gastos = relationship("GastoViaje", back_populates="viaje")
    anticipos = relationship("Anticipo", back_populates="viaje")
    liquidacion = relationship("Liquidacion", back_populates="viaje", uselist=False)
    
    @property
    def ingreso_total_bs(self):
        """Calcula el ingreso total basado en la tarifa"""
        if self.tarifa_tipo == "TON":
            return float(self.peso_ton * self.tarifa_valor)
        elif self.tarifa_tipo == "KM":
            km = self.km_real if self.km_real else self.km_estimado
            return float(km * self.tarifa_valor)
        elif self.tarifa_tipo == "FIJA":
            return float(self.tarifa_valor)
        return 0.0
    
    @property
    def total_gastos_bs(self):
        """Suma total de gastos del viaje"""
        return sum(float(gasto.monto_bs) for gasto in self.gastos if not gasto.deleted_at)
    
    @property
    def margen_bruto_bs(self):
        """Margen bruto del viaje (ingreso - gastos)"""
        return self.ingreso_total_bs - self.total_gastos_bs
    
    @property
    def ruta_completa(self):
        """Retorna la ruta completa del viaje"""
        return f"{self.origen} → {self.destino}"
    
    @property
    def puede_cerrar(self):
        """Indica si el viaje puede ser cerrado"""
        return (self.estado in ["EN_RUTA", "ENTREGADO"] and 
                self.chofer_id and self.vehiculo_id and 
                self.ingreso_total_bs > 0)


class GastoViaje(BaseModel):
    """Modelo de gastos de viajes"""
    __tablename__ = "gastos_viajes"
    
    viaje_id = Column(Integer, ForeignKey("viajes.id"), nullable=False, index=True)
    tipo = Column(String(30), nullable=False)  # COMBUSTIBLE, PEAJE, VIATICO, TALLER, OTRO
    monto_bs = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(String(200))
    soporte_url = Column(String(300))
    fecha = Column(DateTime, nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("tipo IN ('COMBUSTIBLE', 'PEAJE', 'VIATICO', 'TALLER', 'OTRO')", name="ck_gasto_tipo"),
    )
    
    # Relaciones
    viaje = relationship("Viaje", back_populates="gastos")
    
    @property
    def monto_formateado(self):
        """Retorna el monto formateado en bolivianos"""
        return f"Bs {self.monto_bs:,.2f}"