from typing import List
import uuid
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

from models.usuario_rol import usuario_rol


class Rol(Base):
    __tablename__ = "Roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4,
        name="Id"
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, name="Nombre")
    usuarios: Mapped[List["Usuario"]] = relationship(
        "Usuario",
        secondary=usuario_rol,
        back_populates="roles"
    )
