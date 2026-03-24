from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.domain.entities.base import BaseModel
from datetime import datetime


ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Repositorio base con operaciones CRUD comunes"""
    
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Obtener registro por ID"""
        return self.db.query(self.model).filter(
            and_(self.model.id == id, self.model.deleted_at.is_(None))
        ).first()
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Dict[str, Any] = None,
        order_by: str = None
    ) -> List[ModelType]:
        """Obtener todos los registros con paginación y filtros"""
        query = self.db.query(self.model).filter(self.model.deleted_at.is_(None))
        
        # Aplicar filtros
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    attr = getattr(self.model, key)
                    if isinstance(value, str):
                        query = query.filter(attr.ilike(f"%{value}%"))
                    else:
                        query = query.filter(attr == value)
        
        # Aplicar ordenamiento
        if order_by and hasattr(self.model, order_by):
            query = query.order_by(getattr(self.model, order_by))
        
        return query.offset(skip).limit(limit).all()
    
    def count(self, filters: Dict[str, Any] = None) -> int:
        """Contar registros con filtros"""
        query = self.db.query(self.model).filter(self.model.deleted_at.is_(None))
        
        # Aplicar filtros
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    attr = getattr(self.model, key)
                    if isinstance(value, str):
                        query = query.filter(attr.ilike(f"%{value}%"))
                    else:
                        query = query.filter(attr == value)
        
        return query.count()
    
    def create(self, obj_data: Dict[str, Any]) -> ModelType:
        """Crear nuevo registro"""
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, id: int, obj_data: Dict[str, Any]) -> Optional[ModelType]:
        """Actualizar registro existente"""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        
        # Actualizar campos
        for key, value in obj_data.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)
        
        db_obj.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: int) -> bool:
        """Eliminación lógica (soft delete)"""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        
        db_obj.deleted_at = datetime.utcnow()
        self.db.commit()
        return True
    
    def hard_delete(self, id: int) -> bool:
        """Eliminación física del registro"""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True
    
    def exists(self, filters: Dict[str, Any]) -> bool:
        """Verificar si existe un registro con los filtros dados"""
        query = self.db.query(self.model).filter(self.model.deleted_at.is_(None))
        
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        
        return query.first() is not None
    
    def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """Obtener registro por un campo específico"""
        if not hasattr(self.model, field):
            return None
        
        return self.db.query(self.model).filter(
            and_(
                getattr(self.model, field) == value,
                self.model.deleted_at.is_(None)
            )
        ).first()
    
    def get_multiple_by_ids(self, ids: List[int]) -> List[ModelType]:
        """Obtener múltiples registros por IDs"""
        return self.db.query(self.model).filter(
            and_(
                self.model.id.in_(ids),
                self.model.deleted_at.is_(None)
            )
        ).all()
    
    def search(self, search_term: str, search_fields: List[str]) -> List[ModelType]:
        """Búsqueda de texto en múltiples campos"""
        if not search_term or not search_fields:
            return []
        
        query = self.db.query(self.model).filter(self.model.deleted_at.is_(None))
        
        # Crear condiciones de búsqueda para cada campo
        search_conditions = []
        for field in search_fields:
            if hasattr(self.model, field):
                attr = getattr(self.model, field)
                search_conditions.append(attr.ilike(f"%{search_term}%"))
        
        if search_conditions:
            query = query.filter(or_(*search_conditions))
        
        return query.all()
    
    def get_active(self) -> List[ModelType]:
        """Obtener solo registros activos (si el modelo tiene campo 'estado')"""
        query = self.db.query(self.model).filter(self.model.deleted_at.is_(None))
        
        if hasattr(self.model, 'estado'):
            query = query.filter(self.model.estado == 'ACTIVO')
        
        return query.all()
    
    def bulk_create(self, objects_data: List[Dict[str, Any]]) -> List[ModelType]:
        """Crear múltiples registros en lote"""
        db_objects = [self.model(**obj_data) for obj_data in objects_data]
        self.db.add_all(db_objects)
        self.db.commit()
        
        for obj in db_objects:
            self.db.refresh(obj)
        
        return db_objects
    
    def bulk_update(self, updates: List[Dict[str, Any]]) -> bool:
        """Actualizar múltiples registros en lote"""
        try:
            for update_data in updates:
                if 'id' not in update_data:
                    continue
                
                obj_id = update_data.pop('id')
                self.update(obj_id, update_data)
            
            return True
        except Exception:
            self.db.rollback()
            return False