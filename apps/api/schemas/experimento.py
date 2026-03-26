from pydantic import BaseModel
from typing import Optional

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