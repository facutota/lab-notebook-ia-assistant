import json
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CrearProyecto(BaseModel):
    nombre: str
    descripcion: str
    dominio: str
    tags: list[str] = Field(default_factory=list)


class ActualizarProyecto(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    dominio: Optional[str] = None
    tags: Optional[list[str]] = None
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
    dominio: str
    tags: list[str]
    usuario_id: str
    habilitado: bool
    fecha_creacion: datetime
    fecha_modificacion: Optional[datetime] = None
    usuario: UsuarioResponse

    @field_validator('id', 'usuario_id', mode='before')
    @classmethod
    def parse_uuid(cls, v):
        return str(v) if isinstance(v, uuid.UUID) else v

    @field_validator('tags', mode='before')
    @classmethod
    def parse_tags(cls, v):
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                return []
        return []
