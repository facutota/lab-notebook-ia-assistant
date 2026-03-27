from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
import uuid

class CategoriaExperimentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str

class EstadoExperimentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str

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

    @field_validator('id', 'usuario_id', mode='before')
    @classmethod
    def parse_uuid(cls, v):
        return str(v) if isinstance(v, uuid.UUID) else v

class ExperimentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nombre: str
    descripcion: str
    habilitado: bool
    categoria_experimento_id: int
    estado_experimento_id: int
    proyecto_id: str
    fecha_creacion: datetime
    fecha_modificacion: Optional[datetime] = None
    categoria_experimento: CategoriaExperimentoResponse
    estado_experimento: EstadoExperimentoResponse
    proyecto: ProyectoResponse

    @field_validator('id', 'proyecto_id', mode='before')
    @classmethod
    def parse_uuid(cls, v):
        return str(v) if isinstance(v, uuid.UUID) else v

class CrearExperimento(BaseModel):
    nombre: str
    descripcion: str
    categoria_experimento_id: int
    proyecto_id: str

class ActualizarExperimento(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    habilitado: Optional[bool] = None
    categoria_experimento_id: Optional[int] = None
    estado_experimento_id: Optional[int] = None