"""
Services Layer - Punto de entrada principal
Organizado por módulos/entidades.
"""

# Viajes
from app.services.viajes import ViajeService, ViajeEstadisticasService

# Vehículos
from app.services.vehiculos import VehiculoService

# Choferes
from app.services.choferes import ChoferService

# Clientes
from app.services.clientes import ClienteService

# Anticipos
from app.services.anticipos import AnticipoService

# Liquidaciones
from app.services.liquidaciones import LiquidacionService

# Mantenimientos
from app.services.mantenimientos import MantenimientoService


__all__ = [
    # Viajes
    "ViajeService",
    "ViajeEstadisticasService",
    
    # Entidades
    "VehiculoService",
    "ChoferService",
    "ClienteService",
    
    # Operaciones
    "AnticipoService",
    "LiquidacionService",
    "MantenimientoService",
]
