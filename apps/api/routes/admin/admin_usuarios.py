from datetime import datetime
import uuid

from sqlalchemy.orm import Session, joinedload

from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas.usuario import ActualizarUsuarioAdmin, UsuarioAdminResponse
from schemas import PaginationParams, PaginatedResponse
from dependencies.rbac import require_roles
from models.usuario import Usuario
from database import get_db

router = APIRouter(prefix="/admin/usuarios", tags=["admin usuarios"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=PaginatedResponse[UsuarioAdminResponse])
async def lista_usuarios(
    db: Session = Depends(get_db),
    dependencies=Depends(require_roles("Administrador")),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    total = db.query(Usuario).count()
    skip = (page - 1) * limit
    usuarios = db.query(Usuario).order_by(Usuario.fecha_creacion.desc()).offset(skip).limit(limit).all()
    return PaginatedResponse(
        data=usuarios,
        total=total,
        page=page,
        limit=limit,
        total_pages=(total + limit - 1) // limit
    )


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UsuarioAdminResponse)
async def obtener_usuario(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    dependencies=Depends(require_roles("Administrador"))
):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario no encontrado"
        )
    return usuario


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UsuarioAdminResponse)
async def actualizar_perfil_usuario(
    id: uuid.UUID,
    data: ActualizarUsuarioAdmin,
    db: Session = Depends(get_db),
    dependencies=Depends(require_roles("Administrador"))
):
    usuario = db.query(Usuario).options(joinedload(
        Usuario.roles)).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    if data.nombre_completo is not None:
        usuario.nombre_completo = data.nombre_completo
    if data.email is not None:
        email_existente = db.query(Usuario).filter(
            Usuario.email == data.email
        ).first()
        if email_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso"
            )
        usuario.email = data.email
    if data.usa_proveedor is not None:
        usuario.usa_proveedor = data.usa_proveedor

    usuario.fecha_modificacion = datetime.now()

    db.commit()
    db.refresh(usuario)
    return usuario
