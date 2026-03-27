import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from app.database import Base
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
    contenido: Mapped[str] = mapped_column(
        String(255), nullable=False, name="Contenido")
    url_blob: Mapped[str] = mapped_column(
        String(1000), nullable=False, name="UrlBlob")
    ocr_ia_resultado: Mapped[str] = mapped_column(
        String(1000), nullable=False, name="OcrIaResultado")
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, name="FechaRegistro")
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, name="FechaCreacion")
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
