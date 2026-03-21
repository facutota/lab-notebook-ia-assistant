import uuid
from typing import List
from sqlalchemy import ForeignKey, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

class Proyecto(Base):
    __tablename__ = "Proyectos"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4,
        name="Id"
    )
    nombre_proyecto: Mapped[str] = mapped_column(String(255), nullable=False, name="NombreProyecto")
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Usuarios.Id"), name="UsuarioId")
    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="proyectos"
    )
    experimentos: Mapped[List["Experimento"]] = relationship(
        back_populates="proyecto"
    )
