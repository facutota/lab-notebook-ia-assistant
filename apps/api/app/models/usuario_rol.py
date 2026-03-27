from sqlalchemy import Column, ForeignKey, Table

from app.database import Base

usuario_rol = Table(
    "UsuarioRol",
    Base.metadata,
    Column("UsuarioId", ForeignKey("Usuarios.Id"), primary_key=True),
    Column("RolId", ForeignKey("Roles.Id"), primary_key=True)
)
