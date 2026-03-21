# 🏗️ Arquitectura Backend - SRL Transport System

## 📋 Índice
1. [Visión General](#visión-general)
2. [Clean Architecture](#clean-architecture)
3. [Estructura de Carpetas](#estructura-de-carpetas)
4. [Capas y Responsabilidades](#capas-y-responsabilidades)
5. [Patrones Implementados](#patrones-implementados)
6. [Unit of Work](#unit-of-work)
7. [Contrato Frontend-Backend](#contrato-frontend-backend)
8. [Guía de Implementación](#guía-de-implementación)

---

## 📌 Visión General

### Principio Fundamental
> **"El Frontend solo se dedica a maquetación y diseño. TODA la lógica, por mínima que sea, es responsabilidad del Backend."**

### Filosofía de Diseño

| Frontend (Angular) | Backend (FastAPI) |
|-------------------|-------------------|
| Renderizado de UI | Lógica de negocio |
| Formularios/Validación visual | Validación de datos |
| Navegación | Cálculos financieros |
| Llamadas HTTP | Reglas de negocio |
| Manejo de estado UI | Persistencia |
| Diseño responsive | Seguridad y permisos |

---

## 🔷 Clean Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Routes     │  │  Controllers │  │   Schemas    │       │
│  │ (FastAPI)    │  │  (Handlers)  │  │  (Pydantic)  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
├─────────────────────────────────────────────────────────────┤
│                   APPLICATION LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Services   │  │  Use Cases   │  │    DTOs      │       │
│  │ (Orquesta)   │  │ (Casos de Uso)│  │  (Transfer)  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
├─────────────────────────────────────────────────────────────┤
│                     DOMAIN LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Entities   │  │   Domain     │  │   Value      │       │
│  │  (Modelos)   │  │   Services   │  │   Objects    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
├─────────────────────────────────────────────────────────────┤
│                  INFRASTRUCTURE LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Repositories │  │  Unit of     │  │  External    │       │
│  │  (Acceso DB) │  │    Work      │  │  Services    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Carpetas

```
backend/
├── app/
│   ├── api/                          # 🎯 PRESENTATION LAYER
│   │   ├── v1/
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── viajes.py
│   │   │   │   ├── vehiculos.py
│   │   │   │   ├── choferes.py
│   │   │   │   ├── socios.py
│   │   │   │   ├── clientes.py
│   │   │   │   ├── liquidaciones.py
│   │   │   │   ├── anticipos.py
│   │   │   │   ├── mantenimientos.py
│   │   │   │   └── reportes.py
│   │   │   ├── schemas/
│   │   │   │   ├── requests/         # Schemas de entrada
│   │   │   │   │   ├── viaje_request.py
│   │   │   │   │   └── ...
│   │   │   │   └── responses/        # Schemas de salida
│   │   │   │       ├── viaje_response.py
│   │   │   │       ├── paginated_response.py
│   │   │   │       └── ...
│   │   │   └── deps.py               # Dependencias de API
│   │   └── router.py                 # Router principal
│   │
│   ├── application/                  # 🧠 APPLICATION LAYER
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── viaje_service.py
│   │   │   ├── liquidacion_service.py
│   │   │   ├── anticipo_service.py
│   │   │   ├── mantenimiento_service.py
│   │   │   ├── reporte_service.py
│   │   │   └── auth_service.py
│   │   ├── use_cases/
│   │   │   ├── __init__.py
│   │   │   ├── viajes/
│   │   │   │   ├── crear_viaje.py
│   │   │   │   ├── iniciar_viaje.py
│   │   │   │   ├── finalizar_viaje.py
│   │   │   │   └── liquidar_viaje.py
│   │   │   ├── liquidaciones/
│   │   │   │   ├── generar_liquidacion.py
│   │   │   │   └── aprobar_liquidacion.py
│   │   │   └── anticipos/
│   │   │       ├── crear_anticipo.py
│   │   │       └── descontar_anticipo.py
│   │   ├── dtos/
│   │   │   ├── __init__.py
│   │   │   ├── viaje_dto.py
│   │   │   ├── liquidacion_dto.py
│   │   │   └── dashboard_dto.py
│   │   └── interfaces/
│   │       ├── __init__.py
│   │       ├── i_viaje_repository.py
│   │       ├── i_email_service.py
│   │       └── i_storage_service.py
│   │
│   ├── domain/                       # 💎 DOMAIN LAYER (Core)
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── viaje.py
│   │   │   ├── vehiculo.py
│   │   │   ├── chofer.py
│   │   │   ├── socio.py
│   │   │   ├── cliente.py
│   │   │   ├── liquidacion.py
│   │   │   ├── anticipo.py
│   │   │   └── mantenimiento.py
│   │   ├── value_objects/
│   │   │   ├── __init__.py
│   │   │   ├── dinero.py             # Value Object para moneda Bs
│   │   │   ├── ruta.py               # Value Object para rutas
│   │   │   ├── tarifa.py             # Value Object para tarifas
│   │   │   └── periodo.py            # Value Object para períodos
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── calculadora_tarifa.py
│   │   │   ├── calculadora_liquidacion.py
│   │   │   └── validador_viaje.py
│   │   ├── events/
│   │   │   ├── __init__.py
│   │   │   ├── viaje_events.py
│   │   │   └── liquidacion_events.py
│   │   └── exceptions/
│   │       ├── __init__.py
│   │       ├── domain_exception.py
│   │       └── business_rules.py
│   │
│   ├── infrastructure/               # 🔧 INFRASTRUCTURE LAYER
│   │   ├── persistence/
│   │   │   ├── models/               # Modelos SQLAlchemy
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── viaje_model.py
│   │   │   │   └── ...
│   │   │   ├── repositories/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_repository.py
│   │   │   │   ├── viaje_repository.py
│   │   │   │   └── ...
│   │   │   └── unit_of_work.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   └── migrations/
│   │   ├── external/
│   │   │   ├── email_service.py
│   │   │   ├── storage_service.py
│   │   │   └── notification_service.py
│   │   └── security/
│   │       ├── jwt_handler.py
│   │       └── password_handler.py
│   │
│   ├── core/                         # ⚙️ CONFIGURATION
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   └── logging.py
│   │
│   └── main.py                       # Entry Point
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 📚 Capas y Responsabilidades

### 1️⃣ Presentation Layer (API)

**Responsabilidades:**
- Recibir peticiones HTTP
- Validar formato de entrada (Pydantic)
- Delegar a los servicios de aplicación
- Formatear respuestas
- Manejo de errores HTTP

```python
# app/api/v1/routes/viajes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.v1.schemas.responses import ViajeListResponse, ViajeDetailResponse
from app.api.v1.schemas.requests import ViajeCreateRequest, ViajeUpdateRequest
from app.application.services.viaje_service import ViajeService
from app.infrastructure.persistence.unit_of_work import UnitOfWork
from app.api.v1.deps import get_current_user, get_uow

router = APIRouter(prefix="/viajes", tags=["Viajes"])


@router.get("", response_model=ViajeListResponse)
async def listar_viajes(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    estado: str = None,
    fecha_inicio: date = None,
    fecha_fin: date = None,
    uow: UnitOfWork = Depends(get_uow),
    current_user = Depends(get_current_user)
):
    """
    Listar viajes con filtros y paginación.
    TODA la lógica de filtrado está en el servicio.
    """
    service = ViajeService(uow)
    result = service.listar_viajes(
        page=page,
        limit=limit,
        estado=estado,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        usuario=current_user
    )
    return result


@router.post("", response_model=ViajeDetailResponse)
async def crear_viaje(
    request: ViajeCreateRequest,
    uow: UnitOfWork = Depends(get_uow),
    current_user = Depends(get_current_user)
):
    """
    Crear nuevo viaje.
    TODA la validación de negocio está en el servicio.
    """
    service = ViajeService(uow)
    viaje = service.crear_viaje(request, current_user)
    return viaje
```

### 2️⃣ Application Layer (Services)

**Responsabilidades:**
- Orquestar casos de uso
- Coordinar entre entidades
- Manejo de transacciones (UoW)
- Lógica de aplicación (no de dominio)

```python
# app/application/services/viaje_service.py
from typing import Optional
from datetime import date
from app.infrastructure.persistence.unit_of_work import UnitOfWork
from app.domain.services.calculadora_tarifa import CalculadoraTarifa
from app.domain.services.validador_viaje import ValidadorViaje
from app.application.dtos.viaje_dto import ViajeListDTO, ViajeDetailDTO


class ViajeService:
    """Servicio de aplicación para gestión de viajes"""
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.calculadora = CalculadoraTarifa()
        self.validador = ValidadorViaje()
    
    def listar_viajes(
        self,
        page: int,
        limit: int,
        estado: Optional[str] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        usuario = None
    ) -> ViajeListDTO:
        """
        Obtener lista de viajes con filtros.
        Incluye cálculos de totales y estadísticas.
        """
        with self.uow:
            # Obtener viajes
            viajes, total = self.uow.viajes.listar_paginado(
                page=page,
                limit=limit,
                estado=estado,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            
            # Calcular estadísticas (LÓGICA EN BACKEND)
            estadisticas = self._calcular_estadisticas(viajes)
            
            return ViajeListDTO(
                items=viajes,
                total=total,
                page=page,
                limit=limit,
                total_pages=(total + limit - 1) // limit,
                estadisticas=estadisticas
            )
    
    def crear_viaje(self, request, usuario) -> ViajeDetailDTO:
        """
        Crear nuevo viaje con validaciones completas.
        """
        with self.uow:
            # 1. Validar datos de entrada (LÓGICA EN BACKEND)
            self.validador.validar_creacion(request)
            
            # 2. Verificar disponibilidad del vehículo
            vehiculo = self.uow.vehiculos.obtener(request.vehiculo_id)
            if not vehiculo or vehiculo.estado != "DISPONIBLE":
                raise BusinessException("Vehículo no disponible")
            
            # 3. Verificar disponibilidad del chofer
            chofer = self.uow.choferes.obtener(request.chofer_id)
            if not chofer or chofer.estado != "DISPONIBLE":
                raise BusinessException("Chofer no disponible")
            
            # 4. Verificar cliente activo
            cliente = self.uow.clientes.obtener(request.cliente_id)
            if not cliente or cliente.estado != "ACTIVO":
                raise BusinessException("Cliente no activo")
            
            # 5. Calcular tarifa estimada (LÓGICA EN BACKEND)
            tarifa_calculada = self.calculadora.calcular(
                tipo=request.tarifa_tipo,
                valor=request.tarifa_valor,
                peso_ton=request.peso_ton,
                km_estimado=request.km_estimado
            )
            
            # 6. Crear viaje
            viaje = self.uow.viajes.crear({
                **request.dict(),
                "ingreso_estimado_bs": tarifa_calculada,
                "estado": "PLANIFICADO",
                "creado_por": usuario.id
            })
            
            # 7. Actualizar estados
            self.uow.vehiculos.actualizar(vehiculo.id, {"estado": "EN_VIAJE"})
            self.uow.choferes.actualizar(chofer.id, {"estado": "EN_VIAJE"})
            
            # 8. Commit de la transacción
            self.uow.commit()
            
            return ViajeDetailDTO.from_entity(viaje)
    
    def _calcular_estadisticas(self, viajes) -> dict:
        """Calcular estadísticas de los viajes listados"""
        return {
            "total_ingresos_bs": sum(v.ingreso_total_bs for v in viajes),
            "total_gastos_bs": sum(v.total_gastos_bs for v in viajes),
            "margen_total_bs": sum(v.margen_bruto_bs for v in viajes),
            "promedio_km": sum(v.km_estimado for v in viajes) / len(viajes) if viajes else 0,
            "por_estado": self._contar_por_estado(viajes)
        }
    
    def _contar_por_estado(self, viajes) -> dict:
        estados = {}
        for v in viajes:
            estados[v.estado] = estados.get(v.estado, 0) + 1
        return estados
```

### 3️⃣ Domain Layer (Core Business)

**Responsabilidades:**
- Entidades de negocio
- Reglas de negocio puras
- Value Objects
- Domain Services
- Excepciones de dominio

```python
# app/domain/entities/viaje.py
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from app.domain.value_objects.dinero import Dinero
from app.domain.value_objects.ruta import Ruta
from app.domain.value_objects.tarifa import Tarifa


@dataclass
class Viaje:
    """Entidad de dominio para Viaje"""
    id: int
    cliente_id: int
    vehiculo_id: int
    chofer_id: int
    ruta: Ruta
    fecha_salida: datetime
    fecha_llegada: Optional[datetime]
    tipo_carga: str
    peso_ton: Decimal
    volumen_m3: Optional[Decimal]
    tarifa: Tarifa
    estado: str
    km_real: Optional[int] = None
    gastos: List["GastoViaje"] = field(default_factory=list)
    
    @property
    def ingreso_total(self) -> Dinero:
        """Calcula el ingreso total basado en la tarifa"""
        km = self.km_real or self.ruta.km_estimado
        return self.tarifa.calcular_ingreso(self.peso_ton, km)
    
    @property
    def total_gastos(self) -> Dinero:
        """Suma total de gastos del viaje"""
        total = sum(gasto.monto.valor for gasto in self.gastos)
        return Dinero(total)
    
    @property
    def margen_bruto(self) -> Dinero:
        """Margen bruto del viaje"""
        return Dinero(self.ingreso_total.valor - self.total_gastos.valor)
    
    @property
    def puede_iniciar(self) -> bool:
        """Validar si el viaje puede iniciarse"""
        return self.estado == "PLANIFICADO"
    
    @property
    def puede_finalizar(self) -> bool:
        """Validar si el viaje puede finalizarse"""
        return self.estado == "EN_RUTA"
    
    @property
    def puede_liquidar(self) -> bool:
        """Validar si el viaje puede liquidarse"""
        return self.estado == "ENTREGADO" and self.km_real is not None
    
    def iniciar(self) -> None:
        """Iniciar el viaje"""
        if not self.puede_iniciar:
            raise DomainException("El viaje no puede iniciarse en su estado actual")
        self.estado = "EN_RUTA"
    
    def finalizar(self, km_real: int) -> None:
        """Finalizar el viaje"""
        if not self.puede_finalizar:
            raise DomainException("El viaje no puede finalizarse en su estado actual")
        if km_real <= 0:
            raise DomainException("Los kilómetros reales deben ser mayores a 0")
        self.km_real = km_real
        self.fecha_llegada = datetime.utcnow()
        self.estado = "ENTREGADO"
```

```python
# app/domain/value_objects/dinero.py
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class Dinero:
    """Value Object para representar dinero en Bolivianos"""
    valor: Decimal
    moneda: str = "BOB"
    
    def __post_init__(self):
        if not isinstance(self.valor, Decimal):
            object.__setattr__(self, 'valor', Decimal(str(self.valor)))
    
    def __add__(self, other: "Dinero") -> "Dinero":
        if self.moneda != other.moneda:
            raise ValueError("No se pueden sumar diferentes monedas")
        return Dinero(self.valor + other.valor, self.moneda)
    
    def __sub__(self, other: "Dinero") -> "Dinero":
        if self.moneda != other.moneda:
            raise ValueError("No se pueden restar diferentes monedas")
        return Dinero(self.valor - other.valor, self.moneda)
    
    def __mul__(self, factor: Decimal) -> "Dinero":
        return Dinero(self.valor * Decimal(str(factor)), self.moneda)
    
    def redondear(self, decimales: int = 2) -> "Dinero":
        """Redondear el valor"""
        redondeado = self.valor.quantize(
            Decimal(10) ** -decimales, 
            rounding=ROUND_HALF_UP
        )
        return Dinero(redondeado, self.moneda)
    
    @property
    def formateado(self) -> str:
        """Formato legible: Bs 1,234.56"""
        return f"Bs {self.valor:,.2f}"
    
    @property
    def es_positivo(self) -> bool:
        return self.valor > 0
    
    @property
    def es_negativo(self) -> bool:
        return self.valor < 0
```

```python
# app/domain/services/calculadora_liquidacion.py
from decimal import Decimal
from app.domain.value_objects.dinero import Dinero
from app.domain.entities.viaje import Viaje
from app.domain.entities.socio import Socio


class CalculadoraLiquidacion:
    """Domain Service para calcular liquidaciones"""
    
    def calcular(self, viaje: Viaje, socio: Socio) -> dict:
        """
        Calcular liquidación de un viaje.
        TODA la lógica de cálculo está aquí.
        """
        # 1. Ingreso bruto del viaje
        ingreso_bruto = viaje.ingreso_total
        
        # 2. Total de gastos
        total_gastos = viaje.total_gastos
        
        # 3. Margen bruto
        margen_bruto = ingreso_bruto - total_gastos
        
        # 4. Porcentaje del socio según contrato
        porcentaje_socio = Decimal(str(socio.porcentaje_participacion)) / 100
        
        # 5. Pago al socio
        pago_socio = margen_bruto * porcentaje_socio
        
        # 6. Obtener anticipos pendientes del chofer
        anticipos_pendientes = self._obtener_anticipos_pendientes(viaje.chofer_id)
        
        # 7. Saldo del socio (considerando anticipos)
        saldo_socio = pago_socio - anticipos_pendientes
        
        # 8. Comisión empresa
        comision_empresa = margen_bruto - pago_socio
        
        return {
            "viaje_id": viaje.id,
            "ingreso_bs": ingreso_bruto,
            "gastos_bs": total_gastos,
            "margen_bruto_bs": margen_bruto,
            "porcentaje_socio": socio.porcentaje_participacion,
            "pago_socio_bs": pago_socio,
            "anticipos_descontados_bs": anticipos_pendientes,
            "saldo_socio_bs": saldo_socio,
            "comision_empresa_bs": comision_empresa,
            "rentabilidad_pct": self._calcular_rentabilidad(ingreso_bruto, margen_bruto)
        }
    
    def _calcular_rentabilidad(self, ingreso: Dinero, margen: Dinero) -> Decimal:
        """Calcular porcentaje de rentabilidad"""
        if ingreso.valor <= 0:
            return Decimal("0")
        return (margen.valor / ingreso.valor * 100).quantize(Decimal("0.01"))
```

### 4️⃣ Infrastructure Layer

**Responsabilidades:**
- Implementación de repositorios
- Unit of Work
- Servicios externos
- Persistencia de datos

```python
# app/infrastructure/persistence/unit_of_work.py
from sqlalchemy.orm import Session
from app.infrastructure.persistence.repositories import (
    ViajeRepository,
    VehiculoRepository,
    ChoferRepository,
    SocioRepository,
    ClienteRepository,
    LiquidacionRepository,
    AnticipoRepository,
    MantenimientoRepository
)


class UnitOfWork:
    """
    Unit of Work Pattern - Gestiona transacciones de forma atómica.
    Agrupa todas las operaciones de repositorios en una única transacción.
    """
    
    def __init__(self, session_factory):
        self._session_factory = session_factory
        self._session: Session = None
    
    def __enter__(self):
        self._session = self._session_factory()
        self._init_repositories()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        self._session.close()
    
    def _init_repositories(self):
        """Inicializar todos los repositorios con la sesión actual"""
        self.viajes = ViajeRepository(self._session)
        self.vehiculos = VehiculoRepository(self._session)
        self.choferes = ChoferRepository(self._session)
        self.socios = SocioRepository(self._session)
        self.clientes = ClienteRepository(self._session)
        self.liquidaciones = LiquidacionRepository(self._session)
        self.anticipos = AnticipoRepository(self._session)
        self.mantenimientos = MantenimientoRepository(self._session)
    
    def commit(self):
        """Confirmar la transacción"""
        try:
            self._session.commit()
        except Exception as e:
            self.rollback()
            raise e
    
    def rollback(self):
        """Revertir la transacción"""
        self._session.rollback()
    
    @property
    def session(self) -> Session:
        return self._session
```

---

## 🔗 Patrones Implementados

### Repository Pattern (Actual vs Mejorado)

**Estado Actual:** ✅ Ya implementado correctamente
- `BaseRepository` con operaciones CRUD genéricas
- Repositorios específicos por entidad

**Mejoras Propuestas:**
```python
# app/infrastructure/persistence/repositories/viaje_repository.py
from typing import Protocol

# Interface (para dependency injection)
class IViajeRepository(Protocol):
    """Interface del repositorio de viajes"""
    def obtener(self, id: int) -> Optional[Viaje]: ...
    def listar_paginado(self, **filtros) -> tuple[list[Viaje], int]: ...
    def crear(self, data: dict) -> Viaje: ...
    def actualizar(self, id: int, data: dict) -> Viaje: ...
    def eliminar(self, id: int) -> bool: ...


class ViajeRepository(BaseRepository[ViajeModel], IViajeRepository):
    """Implementación del repositorio de viajes"""
    
    def __init__(self, session: Session):
        super().__init__(session, ViajeModel)
    
    def listar_paginado(
        self,
        page: int = 1,
        limit: int = 20,
        estado: str = None,
        fecha_inicio: date = None,
        fecha_fin: date = None,
        vehiculo_id: int = None,
        chofer_id: int = None,
        cliente_id: int = None,
        orden: str = "fecha_salida",
        direccion: str = "desc"
    ) -> tuple[list[Viaje], int]:
        """
        Listar viajes con filtros avanzados y paginación.
        Retorna (items, total_count)
        """
        query = self._base_query()
        
        # Aplicar filtros
        if estado:
            query = query.filter(ViajeModel.estado == estado)
        if fecha_inicio:
            query = query.filter(ViajeModel.fecha_salida >= fecha_inicio)
        if fecha_fin:
            query = query.filter(ViajeModel.fecha_salida <= fecha_fin)
        if vehiculo_id:
            query = query.filter(ViajeModel.vehiculo_id == vehiculo_id)
        if chofer_id:
            query = query.filter(ViajeModel.chofer_id == chofer_id)
        if cliente_id:
            query = query.filter(ViajeModel.cliente_id == cliente_id)
        
        # Contar total
        total = query.count()
        
        # Ordenar y paginar
        orden_attr = getattr(ViajeModel, orden, ViajeModel.fecha_salida)
        if direccion == "desc":
            query = query.order_by(desc(orden_attr))
        else:
            query = query.order_by(asc(orden_attr))
        
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()
        
        return [self._to_entity(m) for m in items], total
```

---

## 🤝 Contrato Frontend-Backend

### Estructura de Respuestas Estándar

```python
# app/api/v1/schemas/responses/base.py
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


class BaseResponse(BaseModel):
    """Respuesta base para todas las operaciones"""
    success: bool = True
    message: Optional[str] = None


class DataResponse(BaseResponse, Generic[T]):
    """Respuesta con datos"""
    data: T


class PaginatedResponse(BaseResponse, Generic[T]):
    """Respuesta paginada"""
    data: List[T]
    pagination: "PaginationMeta"
    estadisticas: Optional[dict] = None


class PaginationMeta(BaseModel):
    """Metadatos de paginación"""
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_prev: bool


class ErrorResponse(BaseModel):
    """Respuesta de error"""
    success: bool = False
    error: str
    code: str
    details: Optional[dict] = None
```

### Endpoints Requeridos por el Frontend

```yaml
# API Endpoints - SRL Transport System

# ==================== AUTH ====================
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
GET    /api/v1/auth/me
PUT    /api/v1/auth/change-password

# ==================== VIAJES ====================
GET    /api/v1/viajes                     # Listar con paginación
GET    /api/v1/viajes/{id}                # Detalle con relaciones
POST   /api/v1/viajes                     # Crear
PUT    /api/v1/viajes/{id}                # Actualizar
DELETE /api/v1/viajes/{id}                # Eliminar (soft)
POST   /api/v1/viajes/{id}/iniciar        # Cambiar estado
POST   /api/v1/viajes/{id}/finalizar      # Cambiar estado + km_real
POST   /api/v1/viajes/{id}/gastos         # Agregar gasto
GET    /api/v1/viajes/estadisticas        # Dashboard stats

# ==================== LIQUIDACIONES ====================
GET    /api/v1/liquidaciones              # Listar
GET    /api/v1/liquidaciones/{id}         # Detalle
POST   /api/v1/liquidaciones              # Generar desde viaje
GET    /api/v1/liquidaciones/pendientes   # Viajes sin liquidar

# ==================== ANTICIPOS ====================
GET    /api/v1/anticipos                  # Listar
GET    /api/v1/anticipos/{id}             # Detalle
POST   /api/v1/anticipos                  # Crear
PUT    /api/v1/anticipos/{id}             # Actualizar
DELETE /api/v1/anticipos/{id}             # Eliminar
GET    /api/v1/anticipos/chofer/{id}      # Por chofer
GET    /api/v1/anticipos/pendientes       # Sin descontar

# ==================== MANTENIMIENTOS ====================
GET    /api/v1/mantenimientos             # Listar
GET    /api/v1/mantenimientos/{id}        # Detalle
POST   /api/v1/mantenimientos             # Crear
PUT    /api/v1/mantenimientos/{id}        # Actualizar
DELETE /api/v1/mantenimientos/{id}        # Eliminar
GET    /api/v1/mantenimientos/vehiculo/{id}    # Por vehículo
GET    /api/v1/mantenimientos/proximos    # Próximos vencimientos

# ==================== VEHÍCULOS ====================
GET    /api/v1/vehiculos                  # Listar
GET    /api/v1/vehiculos/{id}             # Detalle
POST   /api/v1/vehiculos                  # Crear
PUT    /api/v1/vehiculos/{id}             # Actualizar
DELETE /api/v1/vehiculos/{id}             # Eliminar
GET    /api/v1/vehiculos/disponibles      # Solo disponibles
GET    /api/v1/vehiculos/{id}/historial   # Historial viajes

# ==================== CHOFERES ====================
GET    /api/v1/choferes                   # Listar
GET    /api/v1/choferes/{id}              # Detalle
POST   /api/v1/choferes                   # Crear
PUT    /api/v1/choferes/{id}              # Actualizar
DELETE /api/v1/choferes/{id}              # Eliminar
GET    /api/v1/choferes/disponibles       # Solo disponibles
GET    /api/v1/choferes/{id}/viajes       # Historial

# ==================== SOCIOS ====================
GET    /api/v1/socios                     # Listar
GET    /api/v1/socios/{id}                # Detalle
POST   /api/v1/socios                     # Crear
PUT    /api/v1/socios/{id}                # Actualizar
DELETE /api/v1/socios/{id}                # Eliminar
GET    /api/v1/socios/{id}/vehiculos      # Vehículos del socio
GET    /api/v1/socios/{id}/liquidaciones  # Estado cuenta

# ==================== CLIENTES ====================
GET    /api/v1/clientes                   # Listar
GET    /api/v1/clientes/{id}              # Detalle
POST   /api/v1/clientes                   # Crear
PUT    /api/v1/clientes/{id}              # Actualizar
DELETE /api/v1/clientes/{id}              # Eliminar
GET    /api/v1/clientes/{id}/viajes       # Historial

# ==================== REPORTES ====================
GET    /api/v1/reportes/dashboard          # Dashboard principal
GET    /api/v1/reportes/ingresos           # Reporte ingresos
GET    /api/v1/reportes/gastos             # Reporte gastos
GET    /api/v1/reportes/rentabilidad       # Por ruta/cliente
GET    /api/v1/reportes/vehiculos          # Estado flota
GET    /api/v1/reportes/choferes           # Rendimiento

# ==================== EXPORTAR ====================
POST   /api/v1/export/excel                # Exportar a Excel
POST   /api/v1/export/pdf                  # Exportar a PDF
POST   /api/v1/export/csv                  # Exportar a CSV

# ==================== BUSQUEDA GLOBAL ====================
GET    /api/v1/search?q={term}             # Búsqueda global
```

---

## 📋 Guía de Implementación

### Paso 1: Reestructurar Carpetas
```bash
cd backend/app
mkdir -p api/v1/{routes,schemas/requests,schemas/responses}
mkdir -p application/{services,use_cases,dtos,interfaces}
mkdir -p domain/{entities,value_objects,services,events,exceptions}
mkdir -p infrastructure/{persistence/{models,repositories},database,external,security}
```

### Paso 2: Migrar Modelos a Domain/Entities
Separar la lógica de SQLAlchemy de las entidades de dominio.

### Paso 3: Implementar Unit of Work
Agregar el patrón para manejar transacciones atómicas.

### Paso 4: Crear Services Layer
Mover toda la lógica de controllers a services.

### Paso 5: Implementar DTOs
Crear DTOs específicos para comunicación entre capas.

### Paso 6: Actualizar Routes
Simplificar routes para solo delegar a services.

---

## ✅ Checklist de Migración

- [ ] Crear estructura de carpetas Clean Architecture
- [ ] Implementar Unit of Work
- [ ] Migrar entidades de dominio
- [ ] Crear Value Objects (Dinero, Ruta, Tarifa)
- [ ] Implementar Domain Services
- [ ] Crear Application Services
- [ ] Definir DTOs de entrada/salida
- [ ] Actualizar endpoints con nueva estructura
- [ ] Implementar manejo de errores centralizado
- [ ] Agregar logging estructurado
- [ ] Crear tests unitarios por capa
- [ ] Documentar API con OpenAPI

---

## 📝 Notas Finales

### Lo que YA está bien:
- ✅ Repository Pattern implementado
- ✅ Schemas Pydantic separados
- ✅ Modelos con mixins (timestamps, soft delete)
- ✅ Autenticación JWT funcional
- ✅ CORS configurado

### Lo que FALTA:
- ⏳ Unit of Work para transacciones atómicas
- ⏳ Domain Services separados
- ⏳ Value Objects para tipos complejos
- ⏳ Capa Application (Services)
- ⏳ DTOs estructurados
- ⏳ Manejo de errores centralizado
- ⏳ Todos los endpoints CRUD completos

---

*Documento generado para SRL Transport System - Clean Architecture*
