import uuid
from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, Text, Boolean
from database import Base
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
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, name="Nombre")
    descripcion: Mapped[str] = mapped_column(Text, nullable=False, name="Descripcion")
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Usuarios.Id"), name="UsuarioId")
    habilitado: Mapped[bool] = mapped_column(Boolean, default=True, name="Habilitado")
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, name="FechaCreacion")
    fecha_modificacion: Mapped[datetime] = mapped_column(DateTime, nullable=True, name="FechaModificacion")
    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="proyectos"
    )
    experimentos: Mapped[List["Experimento"]] = relationship(
        back_populates="proyecto"
    )
