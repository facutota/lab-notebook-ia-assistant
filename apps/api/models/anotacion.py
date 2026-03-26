import uuid
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Text, Boolean
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER


class Anotacion(Base):
    __tablename__ = "Anotaciones"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4,
        name="Id"
    )
    contenido: Mapped[str] = mapped_column(Text, nullable=False, name="Contenido")
    habilitado: Mapped[bool] = mapped_column(Boolean, default=True, name="Habilitado")
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, name="FechaCreacion")
    fecha_modificacion: Mapped[datetime] = mapped_column(DateTime, nullable=True, name="FechaModificacion")

    usuario_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("Usuarios.Id"),
        name="UsuarioId"
    )
    experimento_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("Experimentos.Id"),
        name="ExperimentoId"
    )
    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="anotaciones"
    )
    experimento: Mapped["Experimento"] = relationship(
        "Experimento",
        back_populates="anotaciones"
    )

    archivos_adjuntos: Mapped[List["ArchivoAdjunto"]] = relationship(back_populates="anotacion")
    comentarios_anotaciones: Mapped[List["ComentarioAnotacion"]] = relationship(back_populates="anotacion")