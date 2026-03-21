"""
Value Objects - Objetos inmutables que representan conceptos del dominio
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional
from datetime import date, datetime


@dataclass(frozen=True)
class Dinero:
    """
    Value Object para representar dinero en Bolivianos.
    Inmutable y con operaciones aritméticas seguras.
    """
    valor: Decimal
    moneda: str = "BOB"  # Boliviano
    
    def __post_init__(self):
        # Convertir a Decimal si no lo es
        if not isinstance(self.valor, Decimal):
            object.__setattr__(self, 'valor', Decimal(str(self.valor)))
    
    def __add__(self, other: "Dinero") -> "Dinero":
        self._validar_misma_moneda(other)
        return Dinero(self.valor + other.valor, self.moneda)
    
    def __sub__(self, other: "Dinero") -> "Dinero":
        self._validar_misma_moneda(other)
        return Dinero(self.valor - other.valor, self.moneda)
    
    def __mul__(self, factor) -> "Dinero":
        return Dinero(self.valor * Decimal(str(factor)), self.moneda)
    
    def __truediv__(self, divisor) -> "Dinero":
        if divisor == 0:
            raise ValueError("No se puede dividir por cero")
        return Dinero(self.valor / Decimal(str(divisor)), self.moneda)
    
    def __lt__(self, other: "Dinero") -> bool:
        self._validar_misma_moneda(other)
        return self.valor < other.valor
    
    def __le__(self, other: "Dinero") -> bool:
        self._validar_misma_moneda(other)
        return self.valor <= other.valor
    
    def __gt__(self, other: "Dinero") -> bool:
        self._validar_misma_moneda(other)
        return self.valor > other.valor
    
    def __ge__(self, other: "Dinero") -> bool:
        self._validar_misma_moneda(other)
        return self.valor >= other.valor
    
    def _validar_misma_moneda(self, other: "Dinero"):
        if self.moneda != other.moneda:
            raise ValueError(f"No se pueden operar {self.moneda} con {other.moneda}")
    
    def redondear(self, decimales: int = 2) -> "Dinero":
        """Redondear al número de decimales especificado"""
        redondeado = self.valor.quantize(
            Decimal(10) ** -decimales,
            rounding=ROUND_HALF_UP
        )
        return Dinero(redondeado, self.moneda)
    
    @property
    def formateado(self) -> str:
        """Formato: Bs 1,234.56"""
        return f"Bs {self.valor:,.2f}"
    
    @property
    def es_positivo(self) -> bool:
        return self.valor > 0
    
    @property
    def es_negativo(self) -> bool:
        return self.valor < 0
    
    @property
    def es_cero(self) -> bool:
        return self.valor == 0
    
    @classmethod
    def cero(cls) -> "Dinero":
        """Factory para crear Dinero con valor cero"""
        return cls(Decimal("0"))
    
    @classmethod
    def desde_float(cls, valor: float) -> "Dinero":
        """Factory para crear desde float"""
        return cls(Decimal(str(valor)))


@dataclass(frozen=True)
class Ruta:
    """Value Object para representar una ruta de viaje"""
    origen: str
    destino: str
    km_estimado: int
    km_real: Optional[int] = None
    
    def __post_init__(self):
        if not self.origen or not self.origen.strip():
            raise ValueError("El origen no puede estar vacío")
        if not self.destino or not self.destino.strip():
            raise ValueError("El destino no puede estar vacío")
        if self.km_estimado <= 0:
            raise ValueError("Los kilómetros estimados deben ser positivos")
    
    @property
    def km_efectivo(self) -> int:
        """Retorna km_real si existe, sino km_estimado"""
        return self.km_real if self.km_real else self.km_estimado
    
    @property
    def descripcion(self) -> str:
        """Descripción legible de la ruta"""
        return f"{self.origen} → {self.destino}"
    
    @property
    def descripcion_completa(self) -> str:
        """Descripción con kilómetros"""
        return f"{self.descripcion} ({self.km_efectivo} km)"
    
    def con_km_real(self, km_real: int) -> "Ruta":
        """Crear nueva Ruta con km_real establecido"""
        return Ruta(self.origen, self.destino, self.km_estimado, km_real)


@dataclass(frozen=True)
class Tarifa:
    """Value Object para representar una tarifa de viaje"""
    tipo: str  # KM, TON, FIJA
    valor: Decimal
    
    TIPOS_VALIDOS = ["KM", "TON", "FIJA"]
    
    def __post_init__(self):
        if self.tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de tarifa debe ser: {', '.join(self.TIPOS_VALIDOS)}")
        if not isinstance(self.valor, Decimal):
            object.__setattr__(self, 'valor', Decimal(str(self.valor)))
        if self.valor <= 0:
            raise ValueError("El valor de la tarifa debe ser positivo")
    
    def calcular_ingreso(self, peso_ton: Decimal, km: int) -> Dinero:
        """Calcular el ingreso según el tipo de tarifa"""
        if self.tipo == "TON":
            return Dinero(peso_ton * self.valor)
        elif self.tipo == "KM":
            return Dinero(Decimal(km) * self.valor)
        elif self.tipo == "FIJA":
            return Dinero(self.valor)
        return Dinero.cero()
    
    @property
    def descripcion(self) -> str:
        """Descripción legible de la tarifa"""
        if self.tipo == "KM":
            return f"Bs {self.valor}/km"
        elif self.tipo == "TON":
            return f"Bs {self.valor}/ton"
        else:
            return f"Bs {self.valor} (fija)"


@dataclass(frozen=True)
class Periodo:
    """Value Object para representar un período de tiempo"""
    fecha_inicio: date
    fecha_fin: date
    
    def __post_init__(self):
        if self.fecha_inicio > self.fecha_fin:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha fin")
    
    @property
    def dias(self) -> int:
        """Número de días en el período"""
        return (self.fecha_fin - self.fecha_inicio).days + 1
    
    @property
    def es_mismo_dia(self) -> bool:
        """Verificar si es un período de un solo día"""
        return self.fecha_inicio == self.fecha_fin
    
    @property
    def es_mes_completo(self) -> bool:
        """Verificar si abarca un mes completo"""
        return (
            self.fecha_inicio.day == 1 and
            self.fecha_fin.month == self.fecha_inicio.month and
            self.fecha_fin.year == self.fecha_inicio.year
        )
    
    def contiene(self, fecha: date) -> bool:
        """Verificar si una fecha está dentro del período"""
        return self.fecha_inicio <= fecha <= self.fecha_fin
    
    def se_superpone(self, otro: "Periodo") -> bool:
        """Verificar si dos períodos se superponen"""
        return not (self.fecha_fin < otro.fecha_inicio or otro.fecha_fin < self.fecha_inicio)
    
    @classmethod
    def mes_actual(cls) -> "Periodo":
        """Factory para crear período del mes actual"""
        hoy = date.today()
        inicio = hoy.replace(day=1)
        # Último día del mes
        if hoy.month == 12:
            fin = hoy.replace(year=hoy.year + 1, month=1, day=1)
        else:
            fin = hoy.replace(month=hoy.month + 1, day=1)
        fin = fin - timedelta(days=1)
        return cls(inicio, fin)
    
    @classmethod
    def año_actual(cls) -> "Periodo":
        """Factory para crear período del año actual"""
        hoy = date.today()
        return cls(
            date(hoy.year, 1, 1),
            date(hoy.year, 12, 31)
        )


@dataclass(frozen=True)
class Porcentaje:
    """Value Object para representar un porcentaje"""
    valor: Decimal
    
    def __post_init__(self):
        if not isinstance(self.valor, Decimal):
            object.__setattr__(self, 'valor', Decimal(str(self.valor)))
        if self.valor < 0 or self.valor > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
    
    def aplicar_a(self, dinero: Dinero) -> Dinero:
        """Aplicar el porcentaje a una cantidad de dinero"""
        return dinero * (self.valor / 100)
    
    @property
    def como_decimal(self) -> Decimal:
        """Retorna el valor como decimal (50% -> 0.5)"""
        return self.valor / 100
    
    @property
    def formateado(self) -> str:
        """Formato: 50.00%"""
        return f"{self.valor:.2f}%"
    
    @classmethod
    def desde_decimal(cls, valor: Decimal) -> "Porcentaje":
        """Factory desde decimal (0.5 -> 50%)"""
        return cls(valor * 100)


# Importar timedelta para Periodo
from datetime import timedelta
