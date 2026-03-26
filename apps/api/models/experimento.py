import uuid
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String, DateTime, Text, Boolean
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER


class Experimento(Base):
    __tablename__ = "Experimentos"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4,
        name="Id"
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, name="Nombre")
    descripcion: Mapped[str] = mapped_column(Text, nullable=False, name="Descripcion")
    habilitado: Mapped[bool] = mapped_column(Boolean, default=True, name="Habilitado")
    categoria_experimento_id: Mapped[int] = mapped_column(
        ForeignKey("CategoriasExperimentos.Id"),
        name="CategoriaExperimentoId"
    )
    estado_experimento_id: Mapped[int] = mapped_column(
        ForeignKey("EstadosExperimentos.Id"),
        name="EstadoExperimentoId"
    )
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, name="FechaCreacion")
    fecha_modificacion: Mapped[datetime] = mapped_column(DateTime, nullable=True, name="FechaModificacion")
    categoria_experimento: Mapped["CategoriaExperimento"] = relationship(
        "CategoriaExperimento",
        back_populates="experimentos"
    )
    estado_experimento: Mapped["EstadoExperimento"] = relationship(
        "EstadoExperimento",
        back_populates="experimentos"
    )
    proyecto_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("Proyectos.Id"),
        name="ProyectoId"
    )
    proyecto: Mapped["Proyecto"] = relationship(
        "Proyecto",
        back_populates="experimentos"
    )
    anotaciones: Mapped[List["Anotacion"]] = relationship(back_populates="experimento")
    comentarios_experimentos: Mapped[List["ComentarioExperimento"]] = relationship(back_populates="experimento")