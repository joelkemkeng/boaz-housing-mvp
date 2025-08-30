"""Update souscriptions table structure

Revision ID: 003
Revises: 002
Create Date: 2024-12-29 23:41:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Supprimer l'ancienne contrainte de clé étrangère
    op.drop_constraint('souscriptions_client_id_fkey', 'souscriptions', type_='foreignkey')
    
    # Supprimer les anciennes colonnes
    op.drop_column('souscriptions', 'client_id')
    op.drop_column('souscriptions', 'date_entree')
    op.drop_column('souscriptions', 'duree_location')
    
    # Ajouter les nouvelles colonnes client
    op.add_column('souscriptions', sa.Column('nom_client', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('prenom_client', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('email_client', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('date_naissance_client', sa.Date(), nullable=False))
    op.add_column('souscriptions', sa.Column('ville_naissance_client', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('pays_naissance_client', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('nationalite_client', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('pays_destination', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('date_arrivee_prevue', sa.Date(), nullable=False))
    
    # Ajouter les colonnes académiques
    op.add_column('souscriptions', sa.Column('ecole_universite', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('filiere', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('pays_ecole', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('ville_ecole', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('code_postal_ecole', sa.String(), nullable=False))
    op.add_column('souscriptions', sa.Column('adresse_ecole', sa.String(), nullable=False))
    
    # Ajouter les nouvelles colonnes logement
    op.add_column('souscriptions', sa.Column('date_entree_prevue', sa.Date(), nullable=False))
    op.add_column('souscriptions', sa.Column('duree_location_mois', sa.Integer(), nullable=False))


def downgrade() -> None:
    # Supprimer les nouvelles colonnes
    op.drop_column('souscriptions', 'duree_location_mois')
    op.drop_column('souscriptions', 'date_entree_prevue')
    op.drop_column('souscriptions', 'adresse_ecole')
    op.drop_column('souscriptions', 'code_postal_ecole')
    op.drop_column('souscriptions', 'ville_ecole')
    op.drop_column('souscriptions', 'pays_ecole')
    op.drop_column('souscriptions', 'filiere')
    op.drop_column('souscriptions', 'ecole_universite')
    op.drop_column('souscriptions', 'date_arrivee_prevue')
    op.drop_column('souscriptions', 'pays_destination')
    op.drop_column('souscriptions', 'nationalite_client')
    op.drop_column('souscriptions', 'pays_naissance_client')
    op.drop_column('souscriptions', 'ville_naissance_client')
    op.drop_column('souscriptions', 'date_naissance_client')
    op.drop_column('souscriptions', 'email_client')
    op.drop_column('souscriptions', 'prenom_client')
    op.drop_column('souscriptions', 'nom_client')
    
    # Réajouter les anciennes colonnes
    op.add_column('souscriptions', sa.Column('duree_location', sa.Integer(), nullable=False))
    op.add_column('souscriptions', sa.Column('date_entree', sa.Date(), nullable=False))
    op.add_column('souscriptions', sa.Column('client_id', sa.Integer(), nullable=False))
    
    # Réajouter la contrainte de clé étrangère
    op.create_foreign_key('souscriptions_client_id_fkey', 'souscriptions', 'clients', ['client_id'], ['id'])