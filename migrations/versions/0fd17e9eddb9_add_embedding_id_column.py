"""Add embedding_id column

Revision ID: 0fd17e9eddb9
Revises: bb97ff8b282c
Create Date: 2023-03-08 01:09:17.279866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fd17e9eddb9'
down_revision = 'bb97ff8b282c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('embeddings', sa.Column('embedding_id', sa.String(), nullable=True))
    op.create_index(op.f('ix_embeddings_embedding_id'), 'embeddings', ['embedding_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_embeddings_embedding_id'), table_name='embeddings')
    op.drop_column('embeddings', 'embedding_id')
    # ### end Alembic commands ###
