import uuid
from typing import List

from sqlalchemy import ForeignKey, String
from app.database import Base
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
    titulo: Mapped[str] = mapped_column(String(255), nullable=False, name="Titulo")
    estado_experimento_id: Mapped[int] = mapped_column(
        ForeignKey("EstadosExperimentos.Id"),
        name="EstadoExperimentoId"
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
