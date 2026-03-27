import uuid
from database import Base
from datetime import datetime

from sqlalchemy import Text, DateTime, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ComentarioExperimento(Base):
    __tablename__ = "ComentarioExperimento"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4,
        name="Id"
    )
    comentario: Mapped[str] = mapped_column(Text, nullable=False, name="Comentario")
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, name="FechaCreacion")
    experimento_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Experimentos.Id"), nullable=False, name="ExperimentoId")
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("Usuarios.Id"),
        name="UsuarioId"
    )
    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="comentario_experimentos"
    )
    experimento: Mapped["Experimento"] = relationship(
        back_populates="comentarios_experimentos"
    )
