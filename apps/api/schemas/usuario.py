from pydantic import BaseModel
from typing import Optional


class UsuarioResponse(BaseModel):
    id: str
    nombre_completo: str

    class Config:
        from_attributes = True
