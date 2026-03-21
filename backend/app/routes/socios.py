"""
Routes - Socios API
"""
from fastapi import APIRouter, Depends, Query, Path
from typing import Optional

from app.core.unit_of_work import UnitOfWork
from app.api.deps import get_uow, get_current_active_user, get_current_admin
from app.models import Usuario

router = APIRouter(prefix="/socios", tags=["Socios"])


@router.get("")
async def listar(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    estado: Optional[str] = None,
    busqueda: Optional[str] = None,
    uow: UnitOfWork = Depends(get_uow),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Listar socios con filtros"""
    with uow:
        query = uow.socios.get_query()
        
        if estado:
            query = query.filter_by(estado=estado)
        if busqueda:
            from sqlalchemy import or_
            from app.models import Socio
            query = query.filter(
                or_(
                    Socio.nombre.ilike(f"%{busqueda}%"),
                    Socio.ci.ilike(f"%{busqueda}%")
                )
            )
        
        total = query.count()
        socios = query.offset((page - 1) * limit).limit(limit).all()
        
        return {
            "data": socios,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }


@router.get("/activos")
async def listar_activos(
    uow: UnitOfWork = Depends(get_uow),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener socios activos para selects"""
    with uow:
        socios = uow.socios.get_all_active()
        return {"data": socios}


@router.get("/{socio_id}")
async def obtener(
    socio_id: int = Path(...),
    uow: UnitOfWork = Depends(get_uow),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener detalle de socio"""
    with uow:
        socio = uow.socios.get_by_id(socio_id)
        if not socio:
            from app.domain.exceptions import EntityNotFoundException
            raise EntityNotFoundException("Socio", socio_id)
        return {"data": socio}


@router.post("", status_code=201)
async def crear(
    datos: dict,
    uow: UnitOfWork = Depends(get_uow),
    current_user: Usuario = Depends(get_current_admin)
):
    """Crear nuevo socio (solo admin)"""
    with uow:
        from app.models import Socio
        socio = Socio(**datos, created_by=current_user.id)
        uow.socios.add(socio)
        uow.commit()
        return {"data": socio, "message": "Socio creado"}


@router.put("/{socio_id}")
async def actualizar(
    socio_id: int,
    datos: dict,
    uow: UnitOfWork = Depends(get_uow),
    current_user: Usuario = Depends(get_current_admin)
):
    """Actualizar socio (solo admin)"""
    with uow:
        socio = uow.socios.get_by_id(socio_id)
        if not socio:
            from app.domain.exceptions import EntityNotFoundException
            raise EntityNotFoundException("Socio", socio_id)
        
        for key, value in datos.items():
            if hasattr(socio, key):
                setattr(socio, key, value)
        
        uow.commit()
        return {"data": socio, "message": "Socio actualizado"}


@router.delete("/{socio_id}")
async def eliminar(
    socio_id: int,
    uow: UnitOfWork = Depends(get_uow),
    current_user: Usuario = Depends(get_current_admin)
):
    """Eliminar socio (solo admin, soft delete)"""
    with uow:
        uow.socios.soft_delete(socio_id)
        uow.commit()
        return {"success": True, "message": "Socio eliminado"}
