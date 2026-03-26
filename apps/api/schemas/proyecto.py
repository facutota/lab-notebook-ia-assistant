from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
import uuid


class CrearProyecto(BaseModel):
    nombre: str
    descripcion: str


class ActualizarProyecto(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    habilitado: Optional[bool] = None


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre_completo: str

    @field_validator('id', mode='before')
    @classmethod
    def parse_uuid(cls, v):
        return str(v) if isinstance(v, uuid.UUID) else v


class ProyectoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre: str
    descripcion: str
    usuario_id: str
    habilitado: bool
    fecha_creacion: datetime
    fecha_modificacion: Optional[datetime] = None
    usuario: UsuarioResponse

    @field_validator('id', 'usuario_id', mode='before')
    @classmethod
    def parse_uuid(cls, v):
        return str(v) if isinstance(v, uuid.UUID) else v
