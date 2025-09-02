"""Add User model with roles and authentication

Revision ID: 005_add_user_model_with_roles
Revises: d023c2536a40
Create Date: 2025-09-02 03:48:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005_add_user_model_with_roles'
down_revision = 'd023c2536a40'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Use existing userrole enum (assume it already exists)
    userrole_enum = sa.Enum('client', 'agent-boaz', 'admin-generale', 'bailleur', name='userrole')
    
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('nom', sa.String(length=100), nullable=False),
        sa.Column('prenom', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', userrole_enum, nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    
    # Drop table
    op.drop_table('users')
    
    # Drop enum
    sa.Enum('client', 'agent-boaz', 'admin-generale', 'bailleur', name='userrole').drop(op.get_bind())