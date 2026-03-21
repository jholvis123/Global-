from pydantic import ConfigDict, BaseModel, field_validator
from typing import Optional
from datetime import datetime, date


class ChoferBase(BaseModel):
    """Schema base para Chofer"""
    nombre: str
    apellido: str
    ci: str
    licencia_numero: str
    licencia_categoria: str
    licencia_vencimiento: date
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    experiencia_anos: int = 0
    estado: str = "ACTIVO"


class ChoferCreate(ChoferBase):
    """Schema para crear Chofer"""
    
    @field_validator("licencia_vencimiento")
    @classmethod
    def validar_licencia_vencimiento(cls, v: date) -> date:
        if v <= date.today():
            raise ValueError("La licencia debe tener fecha de vencimiento futura")
        return v
    
    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: str) -> str:
        if v not in ["ACTIVO", "INACTIVO", "SUSPENDIDO"]:
            raise ValueError("Estado debe ser ACTIVO, INACTIVO o SUSPENDIDO")
        return v
    
    @field_validator("experiencia_anos")
    @classmethod
    def validar_experiencia(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Los años de experiencia no pueden ser negativos")
        return v


class ChoferUpdate(BaseModel):
    """Schema para actualizar Chofer"""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    licencia_numero: Optional[str] = None
    licencia_categoria: Optional[str] = None
    licencia_vencimiento: Optional[date] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    experiencia_anos: Optional[int] = None
    estado: Optional[str] = None
    
    @field_validator("licencia_vencimiento")
    @classmethod
    def validar_licencia_vencimiento(cls, v: Optional[date]) -> Optional[date]:
        if v and v <= date.today():
            raise ValueError("La licencia debe tener fecha de vencimiento futura")
        return v
    
    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in ["ACTIVO", "INACTIVO", "SUSPENDIDO"]:
            raise ValueError("Estado debe ser ACTIVO, INACTIVO o SUSPENDIDO")
        return v


class ChoferResponse(ChoferBase):
    """Schema para respuesta de Chofer"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Propiedades calculadas
    nombre_completo: str
    licencia_vigente: bool
    dias_para_vencer_licencia: int
    licencia_pronta_vencer: bool
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "nombre_completo": "Nombre completo del chofer",
            "licencia_vigente": "Indica si la licencia es vigente",
            "dias_para_vencer_licencia": "Días restantes para que la licencia expire",
            "licencia_pronta_vencer": "Indica si la licencia está próxima a vencer"
        }
    )
        


class ChoferReporte(BaseModel):
    """Schema para reporte de chofer"""
    id: int
    nombre_completo: str
    total_viajes: int
    gastos_viaticos: float
    anticipos_recibidos: float
    desempeño_puntualidad: float
    km_recorridos: int
    
    model_config = ConfigDict(from_attributes=True)