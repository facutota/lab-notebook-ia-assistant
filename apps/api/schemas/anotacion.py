import uuid
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class CrearAnotacion(BaseModel):
    contenido: str
    experimento_id: uuid.UUID


class ActualizarAnotacion(BaseModel):
    contenido: Optional[str] = None
    habilitado: Optional[bool] = None


class AnotacionResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    contenido: str
    usuario_id: str
    experimento_id: str
    habilitado: bool
    fecha_creacion: datetime
    fecha_modificacion: Optional[datetime] = None

    @field_validator('id', 'usuario_id', 'experimento_id', mode='before')
    @classmethod
    def parse_uuid(cls, v):
        return str(v) if isinstance(v, uuid.UUID) else v
