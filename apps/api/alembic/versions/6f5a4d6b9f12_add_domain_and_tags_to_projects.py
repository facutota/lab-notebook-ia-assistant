"""add domain and tags to projects

Revision ID: 6f5a4d6b9f12
Revises: 24c0bbdb8f15
Create Date: 2026-03-26 23:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f5a4d6b9f12'
down_revision: Union[str, Sequence[str], None] = '24c0bbdb8f15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Proyectos', sa.Column('Dominio', sa.String(length=255), nullable=True))
    op.add_column('Proyectos', sa.Column('Tags', sa.Text(), nullable=True))
    op.execute("UPDATE Proyectos SET Dominio = 'other' WHERE Dominio IS NULL")
    op.execute("UPDATE Proyectos SET Tags = '[]' WHERE Tags IS NULL")
    op.alter_column('Proyectos', 'Dominio', existing_type=sa.String(length=255), nullable=False)
    op.alter_column('Proyectos', 'Tags', existing_type=sa.Text(), nullable=False)


def downgrade() -> None:
    op.drop_column('Proyectos', 'Tags')
    op.drop_column('Proyectos', 'Dominio')
