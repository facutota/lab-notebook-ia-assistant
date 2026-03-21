import uuid
from datetime import datetime
from typing import List
from sqlalchemy import Boolean, String, DateTime
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

from app.models import usuario_rol


class Usuario(Base):
    __tablename__ = "Usuarios"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4,
        name="Id"
    )
    nombre_completo: Mapped[str] = mapped_column(String(255), nullable=False, name="NombreCompleto")
    email: Mapped[str] = mapped_column(String(255), nullable=False, name="Email")
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True, name="PasswordHash")
    usa_proveedor: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False, name="UsaProveedor")
    habilitado: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True, name="Habilitado")
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, name="FechaCreacion")
    proyectos: Mapped[List["Proyecto"]] = relationship(back_populates="usuario")
    roles: Mapped[List["Rol"]] = relationship(
        "Rol",
        secondary=usuario_rol,
        back_populates="usuarios"
    )
    anotaciones: Mapped[List["Anotacion"]] = relationship(back_populates="usuario")
