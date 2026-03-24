from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from app.infrastructure.database.database import Base


class TimestampMixin:
    """Mixin para agregar timestamps a los modelos"""

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class SoftDeleteMixin:
    """Mixin para agregar soft delete a los modelos"""

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True)


class BaseModel(Base, TimestampMixin, SoftDeleteMixin):
    """Modelo base con todas las funcionalidades comunes"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)