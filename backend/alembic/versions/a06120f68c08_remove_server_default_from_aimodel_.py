"""Remove server_default from AIModel.model_type

Revision ID: a06120f68c08
Revises: 80428350cb3e
Create Date: 2025-09-13 04:44:58.743964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a06120f68c08'
down_revision: Union[str, Sequence[str], None] = '80428350cb3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('ai_models',
                    'model_type',
                    existing_type=sa.Enum('IMAGE_GENERATION', 'LANGUAGE_MODEL', 'MULTI_MODAL', 'OTHER', name='modeltype'),
                    server_default=None,
                    existing_nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('ai_models',
                    'model_type',
                    existing_type=sa.Enum('IMAGE_GENERATION', 'LANGUAGE_MODEL', 'MULTI_MODAL', 'OTHER', name='modeltype'),
                    server_default='LANGUAGE_MODEL',
                    existing_nullable=False)
