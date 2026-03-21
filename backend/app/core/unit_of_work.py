"""
Unit of Work Pattern
Gestiona transacciones de forma atómica agrupando repositorios.
"""
from typing import Callable
from sqlalchemy.orm import Session
from contextlib import contextmanager

from app.repositories.viaje_repository import ViajeRepository
from app.repositories.socio_repository import SocioRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.vehiculo_repository import VehiculoRepository
from app.repositories.chofer_repository import ChoferRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.liquidacion_repository import LiquidacionRepository
from app.repositories.anticipo_repository import AnticipoRepository
from app.repositories.mantenimiento_repository import MantenimientoRepository


class UnitOfWork:
    """
    Unit of Work - Coordina repositorios en una transacción única.
    
    Uso:
    ```python
    with uow:
        viaje = uow.viajes.crear(data)
        uow.vehiculos.actualizar(id, {"estado": "EN_VIAJE"})
        uow.commit()  # Confirma todo o nada
    ```
    """
    
    def __init__(self, session_factory: Callable[[], Session]):
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
        self.usuarios = UsuarioRepository(self._session)
    
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
    
    def flush(self):
        """Flush sin commit (útil para obtener IDs generados)"""
        self._session.flush()
    
    @property
    def session(self) -> Session:
        """Acceso directo a la sesión (usar con precaución)"""
        return self._session


class UnitOfWorkFactory:
    """Factory para crear instancias de UnitOfWork"""
    
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory
    
    def create(self) -> UnitOfWork:
        """Crear nueva instancia de UnitOfWork"""
        return UnitOfWork(self._session_factory)
    
    @contextmanager
    def begin(self):
        """Context manager para usar UnitOfWork"""
        uow = self.create()
        with uow:
            yield uow
