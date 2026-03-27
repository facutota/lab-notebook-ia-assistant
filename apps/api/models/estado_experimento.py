from typing import List
from sqlalchemy import Integer, String
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class EstadoExperimento(Base):
    __tablename__ = "EstadosExperimentos"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        autoincrement=True,
        name="Id"
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, name="Nombre")
    experimentos: Mapped[List["Experimento"]] = relationship(
        back_populates="estado_experimento"
    )
