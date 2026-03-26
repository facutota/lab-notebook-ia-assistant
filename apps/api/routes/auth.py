from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from auth.jwt_handler import create_access_token, create_refresh_token, decode_token
from auth.utils import verify_password
from config import settings
from database import get_db
from models import Usuario
from schemas.token import Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not user or not verify_password(form_data.password.strip(), user.password_hash.strip()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.habilitado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario se encuentra deshabilitado",
        )
    access_token_expires = timedelta(minutes=settings.token_expire_in_minutes)
    access_token = create_access_token(
        subject=user.email,
        roles=[rol.nombre for rol in user.roles],
        expires_in=access_token_expires
    )
    refresh_token = create_refresh_token(subject=user.email)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str = Body(embed=True), db: Session = Depends(get_db)) -> Any:
    try:
        payload = decode_token(refresh_token)
        email = payload.get("sub")
        token_type = payload.get("token_type")
        
        if not email or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de refresh inválido",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el token de refresh",
        )
    
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not user.habilitado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o deshabilitado",
        )
    
    access_token_expires = timedelta(minutes=settings.token_expire_in_minutes)
    access_token = create_access_token(
        subject=user.email,
        roles=[rol.nombre for rol in user.roles],
        expires_in=access_token_expires
    )
    new_refresh_token = create_refresh_token(subject=user.email)
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
    }

