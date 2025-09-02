"""Add souscription statuses and tracking fields

Revision ID: 006_add_tracking_fields
Revises: 005_add_user_model_with_roles
Create Date: 2025-09-02 02:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '006_add_tracking_fields'
down_revision = '005_add_user_model_with_roles'
branch_labels = None
depends_on = None


def upgrade():
    # Ajouter les nouveaux champs à la table souscriptions
    op.add_column('souscriptions', sa.Column('date_livraison', sa.Date(), nullable=True))
    op.add_column('souscriptions', sa.Column('date_expiration', sa.Date(), nullable=True))
    op.add_column('souscriptions', sa.Column('preuve_paiement_path', sa.String(), nullable=True))
    op.add_column('souscriptions', sa.Column('cree_par_user_id', sa.Integer(), nullable=True))
    
    # Créer la foreign key vers users
    op.create_foreign_key(
        'fk_souscriptions_cree_par_user_id', 
        'souscriptions', 
        'users', 
        ['cree_par_user_id'], 
        ['id']
    )
    
    # Mettre à jour l'enum StatutSouscription pour ajouter ATTENTE_LIVRAISON
    # On doit recréer l'enum avec les nouvelles valeurs
    op.execute("ALTER TYPE statutsouscription ADD VALUE 'ATTENTE_LIVRAISON'")


def downgrade():
    # Supprimer la foreign key
    op.drop_constraint('fk_souscriptions_cree_par_user_id', 'souscriptions', type_='foreignkey')
    
    # Supprimer les colonnes ajoutées
    op.drop_column('souscriptions', 'cree_par_user_id')
    op.drop_column('souscriptions', 'preuve_paiement_path')
    op.drop_column('souscriptions', 'date_expiration')
    op.drop_column('souscriptions', 'date_livraison')
    
    # Note: La suppression de valeurs enum est plus complexe et généralement évitée
    # en production car elle nécessite de vérifier qu'aucun enregistrement n'utilise cette valeur