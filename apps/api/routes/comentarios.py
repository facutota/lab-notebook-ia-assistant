import uuid

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from dependencies.auth import get_current_user
from models import Experimento, Usuario, Proyecto, Anotacion
from models.comentario_experimento import ComentarioExperimento
from models.comentario_anotacion import ComentarioAnotacion
from schemas.comentario import CrearComentario, ComentarioResponse

router = APIRouter(prefix="/comentarios", tags=["comentarios"])


@router.post("/experimento/{experimento_id}", status_code=status.HTTP_201_CREATED, response_model=ComentarioResponse)
async def crear_comentario_experimento(
        experimento_id: uuid.UUID,
        data: CrearComentario,
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
    
    comentario = ComentarioExperimento(
        comentario=data.comentario,
        experimento_id=experimento_id,
        usuario_id=current_user.id
    )
    db.add(comentario)
    db.commit()
    db.refresh(comentario)
    return comentario


@router.post("/anotacion/{anotacion_id}", status_code=status.HTTP_201_CREATED, response_model=ComentarioResponse)
async def crear_comentario_anotacion(
        anotacion_id: uuid.UUID,
        data: CrearComentario,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    anotacion = db.query(Anotacion).filter(Anotacion.id == anotacion_id).first()
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
    
    comentario = ComentarioAnotacion(
        comentario=data.comentario,
        anotacion_id=anotacion_id,
        usuario_id=current_user.id
    )
    db.add(comentario)
    db.commit()
    db.refresh(comentario)
    return comentario


@router.get("/experimento/{experimento_id}", status_code=status.HTTP_200_OK, response_model=list[ComentarioResponse])
async def listar_comentarios_experimento(
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
    
    comentarios = db.query(ComentarioExperimento).filter(
        ComentarioExperimento.experimento_id == experimento_id
    ).all()
    return comentarios


@router.get("/anotacion/{anotacion_id}", status_code=status.HTTP_200_OK, response_model=list[ComentarioResponse])
async def listar_comentarios_anotacion(
        anotacion_id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    anotacion = db.query(Anotacion).filter(Anotacion.id == anotacion_id).first()
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
    
    comentarios = db.query(ComentarioAnotacion).filter(
        ComentarioAnotacion.anotacion_id == anotacion_id
    ).all()
    return comentarios
