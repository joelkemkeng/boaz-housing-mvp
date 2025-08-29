"""Update logements schema to match SQLAlchemy model

Revision ID: 002
Revises: 001
Create Date: 2025-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add missing columns to logements table
    op.add_column('logements', sa.Column('titre', sa.String(length=200), nullable=False, server_default=''))
    op.add_column('logements', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('logements', sa.Column('pays', sa.String(length=100), nullable=False, server_default='France'))
    op.add_column('logements', sa.Column('montant_charges', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('logements', sa.Column('montant_total', sa.Float(), nullable=False, server_default='0.0'))
    
    # Add constraints
    op.create_check_constraint('check_loyer_positive', 'logements', 'loyer > 0')
    op.create_check_constraint('check_charges_positive_ou_nulle', 'logements', 'montant_charges >= 0')
    op.create_check_constraint('check_montant_total_positive', 'logements', 'montant_total > 0')
    op.create_check_constraint('check_coherence_montant_total', 'logements', 'montant_total = loyer + montant_charges')
    op.create_check_constraint('check_titre_non_vide', 'logements', "trim(titre) != ''")
    op.create_check_constraint('check_adresse_non_vide', 'logements', "trim(adresse) != ''")
    op.create_check_constraint('check_ville_non_vide', 'logements', "trim(ville) != ''")
    op.create_check_constraint('check_code_postal_non_vide', 'logements', "trim(code_postal) != ''")
    
    # Remove server_default after adding the column
    op.alter_column('logements', 'titre', server_default=None)
    op.alter_column('logements', 'pays', server_default=None)
    op.alter_column('logements', 'montant_charges', server_default=None)
    op.alter_column('logements', 'montant_total', server_default=None)


def downgrade() -> None:
    # Drop constraints
    op.drop_constraint('check_code_postal_non_vide', 'logements', type_='check')
    op.drop_constraint('check_ville_non_vide', 'logements', type_='check')
    op.drop_constraint('check_adresse_non_vide', 'logements', type_='check')
    op.drop_constraint('check_titre_non_vide', 'logements', type_='check')
    op.drop_constraint('check_coherence_montant_total', 'logements', type_='check')
    op.drop_constraint('check_montant_total_positive', 'logements', type_='check')
    op.drop_constraint('check_charges_positive_ou_nulle', 'logements', type_='check')
    op.drop_constraint('check_loyer_positive', 'logements', type_='check')
    
    # Drop columns
    op.drop_column('logements', 'montant_total')
    op.drop_column('logements', 'montant_charges')
    op.drop_column('logements', 'pays')
    op.drop_column('logements', 'description')
    op.drop_column('logements', 'titre')