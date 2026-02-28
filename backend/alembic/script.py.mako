"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""

from alembic import op
import sqlalchemy as sa

${imports if imports else ""}


# =========================
# REVISION IDENTIFIERS
# =========================

revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


# =========================
# UPGRADE
# =========================

def upgrade():
    """
    Apply schema changes
    """

    ${upgrades if upgrades else "pass"}


# =========================
# DOWNGRADE
# =========================

def downgrade():
    """
    Revert schema changes
    """

    ${downgrades if downgrades else "pass"}