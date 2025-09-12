"""Change prompt template category to enum

Revision ID: bbe406c67418
Revises: 00ed7ece6555
Create Date: 2025-09-11 13:20:23.001627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbe406c67418'
down_revision: Union[str, Sequence[str], None] = '00ed7ece6555'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # First, update existing data to conform to the new enum
    op.execute("UPDATE prompt_templates SET category = 'PROJECT_PROMPT' WHERE category NOT IN ('SYSTEM_PROMPT', 'CHARACTER_PROMPT', 'PROJECT_PROMPT')")

    prompt_category = sa.Enum('SYSTEM_PROMPT', 'CHARACTER_PROMPT', 'PROJECT_PROMPT', name='promptcategory')
    prompt_category.create(op.get_bind(), checkfirst=True)
    
    op.alter_column('prompt_templates', 'category',
               existing_type=sa.VARCHAR(),
               type_=prompt_category,
               existing_nullable=True,
               postgresql_using='category::promptcategory')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('prompt_templates', 'category',
               existing_type=sa.Enum('SYSTEM_PROMPT', 'CHARACTER_PROMPT', 'PROJECT_PROMPT', name='promptcategory'),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    prompt_category = sa.Enum('SYSTEM_PROMPT', 'CHARACTER_PROMPT', 'PROJECT_PROMPT', name='promptcategory')
    prompt_category.drop(op.get_bind())
