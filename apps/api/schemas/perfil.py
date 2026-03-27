from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel

from schemas.rol import RolResponse


class PerfilResponse(BaseModel):
    id: uuid.UUID
    email: str
    nombre_completo: str
    usa_proveedor: bool
    fecha_creacion: datetime
    fecha_modificacion: datetime
    roles: List[RolResponse]

    class Config:
        from_attributes = True

class ActualizarPerfil(BaseModel):
    email: Optional[str] = None
    nombre_completo: Optional[str] = None
    usa_proveedor: Optional[bool] = None
