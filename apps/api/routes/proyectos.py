import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models.proyecto import Proyecto
from models.usuario import Usuario
from schemas.proyecto import CrearProyecto, ProyectoResponse, ActualizarProyecto
from dependencies.auth import get_current_user

router = APIRouter(prefix="/proyectos", tags=["proyectos"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_proyecto(
        proyecto_data: CrearProyecto,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    existe_proyecto = db.query(Proyecto).filter(
        Proyecto.nombre == proyecto_data.nombre).first()
    if existe_proyecto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El proyecto con nombre '{proyecto_data.nombre}' ya existe"
        )

    proyecto = Proyecto(
        nombre=proyecto_data.nombre,
        descripcion=proyecto_data.descripcion,
        usuario_id=current_user.id
    )
    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ProyectoResponse])
async def listar_proyectos(
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):
    proyectos = db.query(Proyecto).options(joinedload(Proyecto.usuario)).filter(
        Proyecto.usuario_id == current_user.id).all()
    return proyectos


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ProyectoResponse)
async def obtener_proyecto(
        id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    proyecto = db.query(Proyecto).options(
        joinedload(Proyecto.usuario)
    ).filter(Proyecto.id == id and Proyecto.usuario_id == current_user.id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto no encontrado"
        )
    if not proyecto or proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este proyecto"
        )
    return proyecto


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ProyectoResponse)
async def actualizar_proyecto(
        id: uuid.UUID,
        proyecto_data: ActualizarProyecto,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    proyecto = db.query(Proyecto).options(
        joinedload(Proyecto.usuario)
    ).filter(Proyecto.id == id and Proyecto.usuario_id == current_user.id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    if not proyecto or proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este proyecto"
        )
    if proyecto_data.nombre is not None:
        proyecto.nombre = proyecto_data.nombre
    if proyecto_data.descripcion is not None:
        proyecto.descripcion = proyecto_data.descripcion
    if proyecto_data.habilitado is not None:
        proyecto.habilitado = proyecto_data.habilitado

    proyecto.fecha_modificacion = datetime.now()

    db.commit()
    db.refresh(proyecto)
    return proyecto


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_proyecto(
        id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    proyecto = db.query(Proyecto).filter(Proyecto.id == id and Proyecto.usuario_id == current_user.id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto no encontrado"
        )
    if not proyecto or proyecto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este proyecto"
        )
    proyecto.habilitado = False
    db.commit()
    db.refresh(proyecto)
    return proyecto
