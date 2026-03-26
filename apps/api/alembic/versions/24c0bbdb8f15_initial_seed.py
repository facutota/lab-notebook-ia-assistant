"""initial seed

Revision ID: 24c0bbdb8f15
Revises: b0fceafd5fa8
Create Date: 2026-03-25 20:59:52.181532

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24c0bbdb8f15'
down_revision: Union[str, Sequence[str], None] = 'b0fceafd5fa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Estados de experimento
    estados = [
        'Activo',
        'Completado',
        'Fallido',
        'Pendiente',
    ]

    for nombre in estados:
        op.execute(
            f"INSERT INTO EstadosExperimentos (Nombre) VALUES ('{nombre}')"
        )

    # Categorías de experimento
    categorias = [
        'Bioquímica',
        'Microbiología',
        'Genética',
        'Farmacología',
        'Otros'
    ]

    for nombre_cat in categorias:
        op.execute(
            f"INSERT INTO CategoriasExperimentos (Nombre) VALUES ('{nombre_cat}')"
        )

    # Rol Investigador
    rol_id = uuid.uuid4()
    op.execute(
        f"INSERT INTO Roles (Id, Nombre) VALUES ('{rol_id}', 'Investigador')"
    )

    # Usuario Investigador Demo
    import bcrypt
    password_hash = bcrypt.hashpw(b'1a2b3c', bcrypt.gensalt()).decode('utf-8')

    usuario_id = uuid.uuid4()
    op.execute(
        f"""INSERT INTO Usuarios (Id, NombreCompleto, Email, PasswordHash, UsaProveedor, Habilitado, FechaCreacion, FechaModificacion) 
        VALUES ('{usuario_id}', 'Investigador Demo', 'investigador@demo.com', '{password_hash}', 0, 1, GETDATE(), GETDATE())"""
    )

    # Relación usuario-rol
    op.execute(
        f"INSERT INTO UsuarioRol (UsuarioId, RolId) VALUES ('{usuario_id}', '{rol_id}')"
    )

    rol_admin_id = uuid.uuid4()
    op.execute(
        f"INSERT INTO Roles (Id, Nombre) VALUES ('{rol_admin_id}', 'Administrador')"
    )

    # Usuario Administrador
    password_hash = bcrypt.hashpw(b'1a2b3c', bcrypt.gensalt()).decode('utf-8')

    usuario_admin_id = uuid.uuid4()
    op.execute(
        f"""INSERT INTO Usuarios (Id, NombreCompleto, Email, PasswordHash, UsaProveedor, Habilitado, FechaCreacion, FechaModificacion) 
            VALUES ('{usuario_admin_id}', 'Administrador Demo', 'admin@demo.com', '{password_hash}', 0, 1, GETDATE(), GETDATE())"""
    )

    # Relación usuario-rol Administrador
    op.execute(
        f"INSERT INTO UsuarioRol (UsuarioId, RolId) VALUES ('{usuario_admin_id}', '{rol_admin_id}')"
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM UsuarioRol WHERE UsuarioId IN (SELECT Id FROM Usuarios WHERE Email = 'investigador@demo.com')")
    op.execute("DELETE FROM Usuarios WHERE Email = 'investigador@demo.com'")
    op.execute("DELETE FROM Roles WHERE Nombre = 'Investigador'")
    op.execute(
        "DELETE FROM CategoriasExperimentos WHERE Nombre IN ('Bioquímica', 'Microbiología', 'Genética', 'Farmacología', 'Otros')")
    op.execute("DELETE FROM EstadosExperimentos WHERE Nombre IN ('Activo', 'Completado', 'Fallido', 'Pendiente')")
    op.execute("DELETE FROM UsuarioRol WHERE UsuarioId IN (SELECT Id FROM Usuarios WHERE Email = 'admin@demo.com')")
    op.execute("DELETE FROM Usuarios WHERE Email = 'admin@demo.com'")
    op.execute("DELETE FROM Roles WHERE Nombre = 'Administrador'")
