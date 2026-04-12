import uuid
from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from dependencies.auth import get_current_user
from models import Anotacion, Usuario, Experimento, Proyecto
from schemas.anotacion import CrearAnotacion, ActualizarAnotacion, AnotacionResponse

router = APIRouter(prefix="/anotaciones", tags=["anotaciones"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_anotacion(
        data: CrearAnotacion,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    experimento = db.query(Experimento).filter(Experimento.id == data.experimento_id).first()
    if not experimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El experimento especificado no existe",
        )
    
    proyecto = db.query(Proyecto).filter(Proyecto.id == experimento.proyecto_id).first()
    if proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este experimento",
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


@router.get("/experimento/{experimento_id}", status_code=status.HTTP_200_OK, response_model=list[AnotacionResponse])
async def listar_anotaciones_por_experimento(
        experimento_id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    experimento = db.query(Experimento).filter(Experimento.id == experimento_id).first()
    if not experimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experimento no encontrado",
        )
    
    proyecto = db.query(Proyecto).filter(Proyecto.id == experimento.proyecto_id).first()
    if proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este experimento",
        )

    anotaciones = db.query(Anotacion).filter(Anotacion.experimento_id == experimento_id).order_by(Anotacion.fecha_creacion).all()
    return anotaciones


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=AnotacionResponse)
async def obtener_anotacion(
        id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    anotacion = db.query(Anotacion).filter(Anotacion.id == id).first()
    if not anotacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anotación no encontrada",
        )
    
    if anotacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a esta anotación",
        )
    
    return anotacion


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=AnotacionResponse)
async def actualizar_anotacion(
        id: uuid.UUID,
        data: ActualizarAnotacion,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    anotacion = db.query(Anotacion).filter(Anotacion.id == id).first()
    if not anotacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anotación no encontrada",
        )
    
    if anotacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a esta anotación",
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
        current_user: Usuario = Depends(get_current_user),
):
    anotacion = db.query(Anotacion).filter(Anotacion.id == id).first()
    if not anotacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anotación no encontrada",
        )
    
    if anotacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a esta anotación",
        )
    
    anotacion.habilitado = False
    db.commit()
    return None
