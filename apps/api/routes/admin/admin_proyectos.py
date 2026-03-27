from datetime import datetime
import uuid

from sqlalchemy.orm import Session, joinedload

from fastapi import APIRouter, Depends, HTTPException, status, Query
from dependencies.rbac import require_roles
from models.usuario import Usuario
from database import get_db
from models.proyecto import Proyecto
from schemas.proyecto import CrearProyecto, ActualizarProyecto, ProyectoResponse
from schemas import PaginationParams, PaginatedResponse

router = APIRouter(prefix="/admin/proyectos", tags=["admin proyectos"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProyectoResponse)
async def crear_proyecto(
        proyecto_data: CrearProyecto,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(require_roles("Administrador")),
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
    return db.query(Proyecto).options(
        joinedload(Proyecto.usuario)
    ).filter(Proyecto.id == proyecto.id).first()


@router.get("/", status_code=status.HTTP_200_OK, response_model=PaginatedResponse[ProyectoResponse])
async def listar_proyectos(
        db: Session = Depends(get_db),
        dependencies=Depends(require_roles("Administrador")),
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100)
):
    total = db.query(Proyecto).count()
    skip = (page - 1) * limit
    proyectos = db.query(Proyecto).options(joinedload(Proyecto.usuario)).order_by(Proyecto.fecha_creacion.desc()).offset(skip).limit(limit).all()
    return PaginatedResponse(
        data=proyectos,
        total=total,
        page=page,
        limit=limit,
        total_pages=(total + limit - 1) // limit
    )


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ProyectoResponse)
async def obtener_proyecto(
        id: uuid.UUID,
        db: Session = Depends(get_db),
        dependencies=Depends(require_roles("Administrador")),
):
    proyecto = db.query(Proyecto).options(
        joinedload(Proyecto.usuario)
    ).filter(Proyecto.id == id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto no encontrado"
        )
    return proyecto


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ProyectoResponse)
async def actualizar_proyecto(
        id: uuid.UUID,
        proyecto_data: ActualizarProyecto,
        db: Session = Depends(get_db),
        dependencies=Depends(require_roles("Administrador")),
):
    proyecto = db.query(Proyecto).options(
        joinedload(Proyecto.usuario)
    ).filter(Proyecto.id == id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
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
        dependencies=Depends(require_roles("Administrador")),
):
    proyecto = db.query(Proyecto).filter(Proyecto.id == id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto no encontrado"
        )

    proyecto.habilitado = False
    db.commit()
    db.refresh(proyecto)
    return proyecto
