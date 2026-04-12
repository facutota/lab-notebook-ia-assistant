from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, field_validator


class UsuarioMeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre_completo: str
    email: str

    @field_validator("id", mode="before")
    @classmethod
    def parse_uuid(cls, v):
        return str(v) if isinstance(v, uuid.UUID) else v


class ActualizarUsuarioMe(BaseModel):
    nombre: str
    apellido: str


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre_completo: str

    @field_validator("id", mode="before")
    @classmethod
    def parse_uuid(cls, v):
        return str(v) if isinstance(v, uuid.UUID) else v


class UsuarioAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nombre_completo: str
    email: str
    usa_proveedor: bool
    habilitado: bool
    fecha_creacion: datetime
    fecha_modificacion: Optional[datetime] = None


class ActualizarUsuarioAdmin(BaseModel):
    email: Optional[str] = None
    nombre_completo: Optional[str] = None
    usa_proveedor: Optional[bool] = None
