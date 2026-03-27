from fastapi import Depends, HTTPException, status
from typing import List

from dependencies.auth import get_current_user
from models.usuario import Usuario


def require_roles(*roles: str):
    def role_checker(user: Usuario = Depends(get_current_user)) -> Usuario:
        user_roles = [rol.nombre.lower() for rol in user.roles]
        required_roles = [rol.lower() for rol in roles]
        
        if not any(rol in user_roles for rol in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No autorizado"
            )
        return user
    return role_checker


def get_current_admin(user: Usuario = Depends(require_roles("admin"))) -> Usuario:
    return user