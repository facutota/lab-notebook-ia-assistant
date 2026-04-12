from datetime import datetime
import uuid

from fastapi import APIRouter, Query, status, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from dependencies.rbac import require_roles
from schemas import PaginatedResponse
from database import get_db
from models import Experimento, Proyecto, Usuario, EstadoExperimento, CategoriaExperimento
from schemas.experimento import CrearExperimento, ActualizarExperimento, ExperimentoResponse

router = APIRouter(prefix="/admin/experimentos", tags=["admin experimentos"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ExperimentoResponse)
async def crear_experimento(
        data: CrearExperimento,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(require_roles("Administrador")),
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
    
    return db.query(Experimento).options(
        joinedload(Experimento.categoria_experimento),
        joinedload(Experimento.estado_experimento),
        joinedload(Experimento.proyecto).joinedload(Proyecto.usuario)
    ).filter(Experimento.id == experimento.id).first()


@router.get("/", status_code=status.HTTP_200_OK, response_model=PaginatedResponse[ExperimentoResponse])
async def listar_proyectos(
        db: Session = Depends(get_db),
        dependencies=Depends(require_roles("Administrador")),
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100)
):
    total = db.query(Experimento).count()
    skip = (page - 1) * limit
    proyectos = db.query(Experimento).options(
        joinedload(Experimento.categoria_experimento),
        joinedload(Experimento.estado_experimento),
        joinedload(Experimento.proyecto).joinedload(Proyecto.usuario)
    ).order_by(Experimento.fecha_creacion.desc()).offset(skip).limit(limit).all()
    return PaginatedResponse(
        data=proyectos,
        total=total,
        page=page,
        limit=limit,
        total_pages=(total + limit - 1) // limit
    )


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ExperimentoResponse)
async def obtener_proyecto(
        id: uuid.UUID,
        db: Session = Depends(get_db),
        dependencies=Depends(require_roles("Administrador")),
):
    experimento = db.query(Experimento).options(
        joinedload(Experimento.categoria_experimento),
        joinedload(Experimento.estado_experimento),
        joinedload(Experimento.proyecto).joinedload(Proyecto.usuario)
    ).filter(Experimento.id == id).first()
    if not experimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experimento no encontrado"
        )
    return experimento


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ExperimentoResponse)
async def actualizar_proyecto(
        id: uuid.UUID,
        proyecto_data: ActualizarExperimento,
        db: Session = Depends(get_db),
        dependencies=Depends(require_roles("Administrador")),
):
    experimento = db.query(Experimento).options(
        joinedload(Experimento.categoria_experimento),
        joinedload(Experimento.estado_experimento),
        joinedload(Experimento.proyecto).joinedload(Proyecto.usuario)
    ).filter(Experimento.id == id).first()
    if not experimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experimento no encontrado"
        )

    if proyecto_data.nombre is not None:
        experimento.nombre = proyecto_data.nombre
    if proyecto_data.descripcion is not None:
        experimento.descripcion = proyecto_data.descripcion
    if proyecto_data.habilitado is not None:
        experimento.habilitado = proyecto_data.habilitado

    experimento.fecha_modificacion = datetime.now()

    db.commit()
    db.refresh(experimento)
    return experimento


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_proyecto(
        id: uuid.UUID,
        db: Session = Depends(get_db),
        dependencies=Depends(require_roles("Administrador")),
):
    experimento = db.query(Experimento).filter(Experimento.id == id).first()
    if not experimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experimento no encontrado"
        )

    experimento.habilitado = False
    db.commit()
    db.refresh(experimento)
    return experimento