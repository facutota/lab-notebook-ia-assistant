from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies.auth import get_current_user
from models.usuario import Usuario
from schemas.usuario import ActualizarUsuarioMe, UsuarioMeResponse

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UsuarioMeResponse)
async def obtener_mi_perfil(
        current_user: Usuario = Depends(get_current_user),
):
    return current_user


@router.put("/me", status_code=status.HTTP_200_OK, response_model=UsuarioMeResponse)
async def actualizar_mi_perfil(
        data: ActualizarUsuarioMe,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
):
    current_user.nombre_completo = f"{data.nombre.strip()} {data.apellido.strip()}".strip()
    current_user.fecha_modificacion = datetime.now()
    db.commit()
    db.refresh(current_user)
    return current_user
