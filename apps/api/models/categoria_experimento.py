from typing import List

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column
from database import Base


class CategoriaExperimento(Base):
    __tablename__ = "CategoriasExperimentos"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        autoincrement=True,
        name="Id"
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, name="Nombre")
    experimentos: Mapped[List["Experimento"]] = relationship(
        back_populates="categoria_experimento"
    )
