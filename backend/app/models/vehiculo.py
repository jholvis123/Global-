from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from app.models.base import BaseModel


class Vehiculo(BaseModel):
    """Modelo de vehículos (camiones)"""
    __tablename__ = "vehiculos"
    
    placa = Column(String(10), unique=True, nullable=False, index=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    año = Column(Integer, nullable=False)
    capacidad_ton = Column(Numeric(6, 2), nullable=False)
    socio_id = Column(Integer, ForeignKey("socios.id"), nullable=False, index=True)
    estado = Column(String(20), default="ACTIVO", nullable=False)  # ACTIVO, MANTENIMIENTO, BAJA
    soat_vencimiento = Column(Date)
    itv_vencimiento = Column(Date)
    seguro_vencimiento = Column(Date)
    
    # Relaciones
    socio = relationship("Socio", back_populates="vehiculos")
    viajes = relationship("Viaje", back_populates="vehiculo")
    mantenimientos = relationship("Mantenimiento", back_populates="vehiculo")
    remolques = relationship("Remolque", back_populates="vehiculo")
    
    @property
    def identificacion_completa(self):
        """Retorna la identificación completa del vehículo"""
        return f"{self.placa} - {self.marca} {self.modelo} ({self.año})"
    
    @property
    def documentos_vigentes(self):
        """Verifica si todos los documentos están vigentes"""
        hoy = date.today()
        soat_vigente = not self.soat_vencimiento or self.soat_vencimiento >= hoy
        itv_vigente = not self.itv_vencimiento or self.itv_vencimiento >= hoy
        seguro_vigente = not self.seguro_vencimiento or self.seguro_vencimiento >= hoy
        return soat_vigente and itv_vigente and seguro_vigente
    
    @property
    def documentos_por_vencer(self):
        """Lista de documentos que vencen en los próximos 30 días"""
        hoy = date.today()
        documentos = []
        
        if self.soat_vencimiento and 0 <= (self.soat_vencimiento - hoy).days <= 30:
            documentos.append(("SOAT", self.soat_vencimiento))
        if self.itv_vencimiento and 0 <= (self.itv_vencimiento - hoy).days <= 30:
            documentos.append(("ITV", self.itv_vencimiento))
        if self.seguro_vencimiento and 0 <= (self.seguro_vencimiento - hoy).days <= 30:
            documentos.append(("SEGURO", self.seguro_vencimiento))
            
        return documentos


class Remolque(BaseModel):
    """Modelo de remolques/semirremolques"""
    __tablename__ = "remolques"
    
    placa = Column(String(10), unique=True, nullable=False, index=True)
    tipo = Column(String(50), nullable=False)
    capacidad_ton = Column(Numeric(6, 2), nullable=False)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=True)
    estado = Column(String(20), default="ACTIVO", nullable=False)  # ACTIVO, MANTENIMIENTO, BAJA
    
    # Relaciones
    vehiculo = relationship("Vehiculo", back_populates="remolques")
    
    @property
    def identificacion_completa(self):
        """Retorna la identificación completa del remolque"""
        return f"{self.placa} - {self.tipo}"