"""create all

Revision ID: 80c096c08445
Revises: 
Create Date: 2023-05-01 19:32:37.148594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80c096c08445'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create sensors table
    op.create_table(
        'sensors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(20), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create readings table
    op.create_table(
        'readings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(20), nullable=False),
        sa.Column('reading', sa.String(40), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('sensor_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create foreign key constraints with back references
    op.create_foreign_key('sensors_owner_fkey', 'sensors', 'users', ['user_id'], ['id'], ondelete='CASCADE', source_schema='public', referent_schema='public')
    op.create_foreign_key('readings_sensor_fkey', 'readings', 'sensors', ['sensor_id'], ['id'], ondelete='CASCADE', source_schema='public', referent_schema='public')
    op.create_foreign_key('readings_owner_fkey', 'readings', 'users', ['user_id'], ['id'], ondelete='CASCADE', source_schema='public', referent_schema='public')
    op.add_column('sensors', sa.Column('readings_id', sa.Integer(), nullable=True), schema='public')
    op.create_foreign_key('fk_sensors_readings_id_readings', 'sensors', 'readings', ['readings_id'], ['id'], ondelete='CASCADE', source_schema='public', referent_schema='public')
    op.create_index(op.f('ix_sensors_readings_id'), 'sensors', ['readings_id'], unique=False, schema='public')







def downgrade():
    # Drop relationships from models
    op.drop_constraint('sensors_user_id_fkey', 'sensors', type_='foreignkey')
    op.drop_relationship('sensors_owner', 'sensors', 'users')
    op.drop_relationship('readings_sensor', 'readings', 'sensors')
    op.drop_relationship('readings_owner', 'readings', 'users')

    # Drop readings table
    op.drop_table('readings')

    # Drop sensors table
    op.drop_table('sensors')

    # Drop users table
    op.drop_table('users')
