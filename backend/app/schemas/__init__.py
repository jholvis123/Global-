from pydantic import ConfigDict
from .usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, LoginRequest, TokenResponse
from .socio import SocioCreate, SocioUpdate, SocioResponse
from .chofer import ChoferCreate, ChoferUpdate, ChoferResponse
from .cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from .vehiculo import VehiculoCreate, VehiculoUpdate, VehiculoResponse
from .viaje import ViajeCreate, ViajeUpdate, ViajeResponse, GastoViajeCreate
from .anticipo import AnticipoCreate, AnticipoResponse
from .liquidacion import LiquidacionResponse
from .mantenimiento import MantenimientoCreate, MantenimientoResponse
from .reportes import ReporteDiario, ReporteMensual, ReporteTipoCarga

__all__ = [
    # Usuario/Auth
    "UsuarioCreate", "UsuarioUpdate", "UsuarioResponse", 
    "LoginRequest", "TokenResponse",
    
    # Entidades principales
    "SocioCreate", "SocioUpdate", "SocioResponse",
    "ChoferCreate", "ChoferUpdate", "ChoferResponse", 
    "ClienteCreate", "ClienteUpdate", "ClienteResponse",
    "VehiculoCreate", "VehiculoUpdate", "VehiculoResponse",
    "ViajeCreate", "ViajeUpdate", "ViajeResponse", "GastoViajeCreate",
    "AnticipoCreate", "AnticipoResponse",
    "LiquidacionResponse",
    "MantenimientoCreate", "MantenimientoResponse",
    
    # Reportes
    "ReporteDiario", "ReporteMensual", "ReporteTipoCarga"
]