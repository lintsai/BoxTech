"""add indices for videos list filters

Revision ID: 3fde56e316f3
Revises: 
Create Date: 2025-11-05 09:37:28.411430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fde56e316f3'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # videos 表的索引
    op.create_index("ix_videos_upload_date", "videos", ["upload_date"], unique=False)
    op.create_index("ix_videos_training_date", "videos", ["training_date"], unique=False)
    op.create_index("ix_videos_location", "videos", ["location"], unique=False)
    op.create_index("ix_videos_training_type", "videos", ["training_type"], unique=False)

def downgrade():
    op.drop_index("ix_videos_training_type", table_name="videos")
    op.drop_index("ix_videos_location", table_name="videos")
    op.drop_index("ix_videos_training_date", table_name="videos")
    op.drop_index("ix_videos_upload_date", table_name="videos")