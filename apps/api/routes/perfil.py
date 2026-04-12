

from datetime import datetime

from dependencies.auth import get_current_user
from models.usuario import Usuario
from schemas.perfil import ActualizarPerfil, PerfilResponse
from database import get_db
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix="/perfil", tags=["perfil"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=PerfilResponse)
async def obtener_perfil_usuario(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):

    usuario = db.query(Usuario).options(joinedload(Usuario.roles)).filter(
        Usuario.id == current_user.id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.put("/", status_code=status.HTTP_200_OK, response_model=PerfilResponse)
async def actualizar_perfil_usuario(
    data: ActualizarPerfil,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    usuario = db.query(Usuario).options(joinedload(Usuario.roles)).filter(Usuario.id == current_user.id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    if data.nombre_completo is not None:
        usuario.nombre_completo = data.nombre_completo
    if data.email is not None:
        email_existente = db.query(Usuario).filter(
            Usuario.email == data.email,
            Usuario.id != current_user.id
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