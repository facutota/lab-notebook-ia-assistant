import uuid
from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from dependencies.rbac import require_roles
from database import get_db
from models import Anotacion, Usuario, Experimento, Proyecto
from schemas.anotacion import CrearAnotacion, ActualizarAnotacion, AnotacionResponse
from schemas import PaginatedResponse


router = APIRouter(prefix="/admin/anotaciones", tags=["anotaciones"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_anotacion(
        data: CrearAnotacion,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(require_roles("Administrador")),
):
    experimento = db.query(Experimento).filter(
        Experimento.id == data.experimento_id).first()
    if not experimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El experimento especificado no existe",
        )

    anotacion = Anotacion(
        contenido=data.contenido,
        usuario_id=current_user.id,
        experimento_id=data.experimento_id
    )

    db.add(anotacion)
    db.commit()
    db.refresh(anotacion)
    return anotacion


@router.get("/experimento/{experimento_id}", status_code=status.HTTP_200_OK, response_model=PaginatedResponse[AnotacionResponse])
async def listar_anotaciones_por_experimento(
        experimento_id: uuid.UUID,
        db: Session = Depends(get_db),
        dependencies=Depends(require_roles("Administrador")),
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100)
):
    experimento = db.query(Experimento).filter(
        Experimento.id == experimento_id).first()
    if not experimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experimento no encontrado",
        )

    total = db.query(Anotacion).filter(Anotacion.experimento_id == experimento_id).count()
    skip = (page - 1) * limit
    anotaciones = db.query(Anotacion).filter(
        Anotacion.experimento_id == experimento_id).order_by(Anotacion.fecha_creacion.desc()).offset(skip).limit(limit).all()
    return PaginatedResponse(
        data=anotaciones,
        total=total,
        page=page,
        limit=limit,
        total_pages=(total + limit - 1) // limit
    )


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=AnotacionResponse)
async def obtener_anotacion(
        id: uuid.UUID,
        db: Session = Depends(get_db),
        dependencies=Depends(require_roles("Administrador")),
):
    anotacion = db.query(Anotacion).filter(Anotacion.id == id).first()
    if not anotacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anotación no encontrada",
        )

    return anotacion


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=AnotacionResponse)
async def actualizar_anotacion(
        id: uuid.UUID,
        data: ActualizarAnotacion,
        db: Session = Depends(get_db),
        dependencies=Depends(require_roles("Administrador")),
):
    anotacion = db.query(Anotacion).filter(Anotacion.id == id).first()
    if not anotacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anotación no encontrada",
        )

    if data.contenido is not None:
        anotacion.contenido = data.contenido
    if data.habilitado is not None:
        anotacion.habilitado = data.habilitado

    anotacion.fecha_modificacion = datetime.now()

    db.commit()
    db.refresh(anotacion)
    return anotacion


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deshabilitar_anotacion(
        id: uuid.UUID,
        db: Session = Depends(get_db),
        dependencies=Depends(require_roles("Administrador")),
):
    anotacion = db.query(Anotacion).filter(Anotacion.id == id).first()
    if not anotacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anotación no encontrada",
        )

    anotacion.habilitado = False
    db.commit()
    return None
