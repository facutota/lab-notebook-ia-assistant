import uuid
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class CrearComentario(BaseModel):
    comentario: str


class ComentarioResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    comentario: str
    usuario_id: str
    experimento_id: Optional[str] = None
    anotacion_id: Optional[str] = None
    fecha_creacion: datetime

    @field_validator('id', 'usuario_id', 'experimento_id', 'anotacion_id', mode='before')
    @classmethod
    def parse_uuid(cls, v):
        return str(v) if isinstance(v, uuid.UUID) else v
