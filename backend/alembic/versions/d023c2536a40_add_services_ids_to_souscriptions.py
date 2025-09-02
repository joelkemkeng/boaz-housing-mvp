"""Add services_ids to souscriptions

Revision ID: d023c2536a40
Revises: 004
Create Date: 2025-08-31 22:50:01.185392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd023c2536a40'
down_revision: Union[str, None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ajouter la colonne services_ids avec valeur par défaut [1]
    op.add_column('souscriptions', sa.Column('services_ids', sa.JSON(), nullable=True))
    
    # Mettre à jour toutes les souscriptions existantes avec [1] par défaut
    op.execute("UPDATE souscriptions SET services_ids = '[1]' WHERE services_ids IS NULL")


def downgrade() -> None:
    # Supprimer la colonne services_ids
    op.drop_column('souscriptions', 'services_ids')
