import uuid
from datetime import datetime

from sqlalchemy import Text, DateTime, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class ArchivoAdjunto(Base):
    __tablename__ = "ArchivosAdjuntos"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4,
        name="Id"
    )

    url_blob: Mapped[str] = mapped_column(
        Text, nullable=False, name="UrlBlob")
    anotacion_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Anotaciones.Id"), nullable=False, name="AnotacionId")
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, name="FechaCreacion")
    fecha_modificacion: Mapped[datetime] = mapped_column(DateTime, nullable=True, name="FechaModificacion")
    anotacion: Mapped["Anotacion"] = relationship(
        back_populates="archivos_adjuntos"
    )
