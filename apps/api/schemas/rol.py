import uuid

from pydantic import BaseModel


class RolResponse(BaseModel):
    id: uuid.UUID
    nombre: str

    class Config:
        from_attributes = True