import uuid
from datetime import datetime

from sqlalchemy import Text, DateTime, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ComentarioAnotacion(Base):
    __tablename__ = "ComentarioAnotacion"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4,
        name="Id"
    )
    comentario: Mapped[str] = mapped_column(Text, nullable=False, name="Comentario")
    fechaCreacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, name="FechaCreacion" )
    anotacion_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Anotaciones.Id"), nullable=False, name="AnotacionId")
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("Usuarios.Id"),
        name="UsuarioId"
    )
    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="comentario_anotaciones"
    )
    anotacion: Mapped["Anotacion"] = relationship(
        back_populates="comentarios_anotaciones"
    )
