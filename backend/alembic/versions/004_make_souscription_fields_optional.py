"""Make souscription fields optional

Revision ID: 004
Revises: 003
Create Date: 2024-12-29 23:25:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rendre optionnels les champs qui ne sont pas critiques
    op.alter_column('souscriptions', 'date_naissance_client', nullable=True)
    op.alter_column('souscriptions', 'ville_naissance_client', nullable=True)
    op.alter_column('souscriptions', 'pays_naissance_client', nullable=True)
    op.alter_column('souscriptions', 'nationalite_client', nullable=True)
    op.alter_column('souscriptions', 'pays_destination', nullable=True)
    op.alter_column('souscriptions', 'date_arrivee_prevue', nullable=True)
    op.alter_column('souscriptions', 'pays_ecole', nullable=True)
    op.alter_column('souscriptions', 'ville_ecole', nullable=True)
    op.alter_column('souscriptions', 'code_postal_ecole', nullable=True)
    op.alter_column('souscriptions', 'adresse_ecole', nullable=True)
    op.alter_column('souscriptions', 'date_entree_prevue', nullable=True)


def downgrade() -> None:
    # Remettre les contraintes NOT NULL
    op.alter_column('souscriptions', 'date_entree_prevue', nullable=False)
    op.alter_column('souscriptions', 'adresse_ecole', nullable=False)
    op.alter_column('souscriptions', 'code_postal_ecole', nullable=False)
    op.alter_column('souscriptions', 'ville_ecole', nullable=False)
    op.alter_column('souscriptions', 'pays_ecole', nullable=False)
    op.alter_column('souscriptions', 'date_arrivee_prevue', nullable=False)
    op.alter_column('souscriptions', 'pays_destination', nullable=False)
    op.alter_column('souscriptions', 'nationalite_client', nullable=False)
    op.alter_column('souscriptions', 'pays_naissance_client', nullable=False)
    op.alter_column('souscriptions', 'ville_naissance_client', nullable=False)
    op.alter_column('souscriptions', 'date_naissance_client', nullable=False)