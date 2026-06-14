"""add cascade deletes

Revision ID: 1fed88067c67
Revises: 7c432d8618f3
Create Date: 2026-06-14 20:33:45.681290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '1fed88067c67'
down_revision: Union[str, Sequence[str], None] = '7c432d8618f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('comment', schema=None, recreate="always") as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_comment_user_id_user'), 'user', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(batch_op.f('fk_comment_book_id_book'), 'book', ['book_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('file', schema=None, recreate="always") as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_file_book_id_book'), 'book', ['book_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('selection', schema=None, recreate="always") as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_selection_user_id_user'), 'user', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    with op.batch_alter_table('selection', schema=None, recreate="always") as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_selection_user_id_user'), type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_selection_user_id_user'), 'user', ['user_id'], ['id'])

    with op.batch_alter_table('file', schema=None, recreate="always") as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_file_book_id_book'), type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_file_book_id_book'), 'book', ['book_id'], ['id'])

    with op.batch_alter_table('comment', schema=None, recreate="always") as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_comment_user_id_user'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_comment_book_id_book'), type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_comment_user_id_user'), 'user', ['user_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_comment_book_id_book'), 'book', ['book_id'], ['id'])