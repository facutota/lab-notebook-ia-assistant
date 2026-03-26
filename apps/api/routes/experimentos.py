import uuid

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from dependencies.auth import get_current_user
from models import Experimento, Usuario, EstadoExperimento, Proyecto, CategoriaExperimento
from schemas.experimento import CrearExperimento, ActualizarExperimento

router = APIRouter(prefix="/experimentos", tags=["experimentos"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_experimento(
        data: CrearExperimento,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    existe_experimento = db.query(Experimento).filter(Experimento.nombre == data.nombre).first()
    if existe_experimento:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El experimento con nombre '{data.nombre}' ya existe"
        )
    proyecto = db.query(Proyecto).filter(Proyecto.id == data.proyecto_id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    if not proyecto.habilitado:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El proyecto está deshabilitado"
        )

    categoria = db.query(CategoriaExperimento).filter(CategoriaExperimento.id == data.categoria_experimento_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría de experimento no es válida"
        )

    estado_activo = db.query(EstadoExperimento).filter(EstadoExperimento.nombre == 'Activo').first()

    experimento = Experimento(
        nombre=data.nombre,
        descripcion=data.descripcion,
        categoria_experimento_id=data.categoria_experimento_id,
        estado_experimento_id=estado_activo.id,
        proyecto_id=data.proyecto_id,
    )
    db.add(experimento)
    db.commit()
    db.refresh(experimento)
    return experimento


@router.get("/proyecto/{id}", status_code=status.HTTP_200_OK)
async def listar_experimentos(
        id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    proyecto = db.query(Proyecto).filter(Proyecto.id == id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    if proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este proyecto"
        )

    experimentos = db.query(Experimento).options(
        joinedload(Experimento.estado_experimento),
        joinedload(Experimento.categoria_experimento)
    ).filter(Experimento.proyecto_id == id).all()

    return experimentos


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def obtener_experimento(
        id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    experimento = db.query(Experimento).options(
        joinedload(Experimento.estado_experimento),
        joinedload(Experimento.categoria_experimento)
    ).filter(Experimento.id == id).first()

    if not experimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experimento no encontrado"
        )
    proyecto = db.query(Proyecto).filter(Proyecto.id == experimento.proyecto_id).first()
    if not proyecto or proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este proyecto"
        )

    return experimento


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_experimento(
        id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    experimento = db.query(Experimento).filter(Experimento.id == id).first()
    if not experimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experimento no encontrado"
        )
    proyecto = db.query(Proyecto).filter(Proyecto.id == experimento.proyecto_id).first()
    if not proyecto.habilitado:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El proyecto está deshabilitado"
        )
    if not proyecto or proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este proyecto"
        )
    experimento.habilitado = False
    db.commit()
    db.refresh(experimento)
    return experimento


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_experimento(
        id: uuid.UUID,
        data: ActualizarExperimento,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    experimento = db.query(Experimento).filter(Experimento.id == id).first()
    if not experimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experimento no encontrado"
        )
    proyecto = db.query(Proyecto).filter(Proyecto.id == experimento.proyecto_id).first()
    if not proyecto.habilitado:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El proyecto está deshabilitado"
        )
    if not proyecto or proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este proyecto"
        )

    if data.nombre is not None:
        experimento.nombre = data.nombre
    if data.descripcion is not None:
        experimento.descripcion = data.descripcion
    if data.habilitado is not None:
        experimento.habilitado = data.habilitado
    if data.estado_experimento_id is not None:
        experimento.estado_experimento_id = data.estado_experimento_id
    if data.categoria_experimento_id is not None:
        experimento.categoria_experimento_id = data.categoria_experimento_id
    db.commit()
    db.refresh(experimento)
    return experimento
