"""Initial schema with all tables

Revision ID: 001
Revises:
Create Date: 2024-02-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create source_schema table
    op.create_table(
        "source_schema",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_system", sa.String(length=255), nullable=False),
        sa.Column("source_schema", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.Column("updated_by", sa.String(length=255), nullable=True),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_source_schema_id"), "source_schema", ["id"], unique=False)
    op.create_index(
        op.f("ix_source_schema_source_system"), "source_schema", ["source_system"], unique=False
    )

    # Create subscription table
    op.create_table(
        "subscription",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("gcp_subscription_id", sa.String(length=255), nullable=False),
        sa.Column("subscription_name", sa.String(length=255), nullable=False),
        sa.Column("project_id", sa.String(length=255), nullable=False),
        sa.Column("topic_id", sa.String(length=255), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.Column("updated_by", sa.String(length=255), nullable=True),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("gcp_subscription_id"),
    )
    op.create_index(op.f("ix_subscription_id"), "subscription", ["id"], unique=False)

    # Create pipeline table
    op.create_table(
        "pipeline",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("connector_id", sa.String(length=255), nullable=True),
        sa.Column("created_by", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.Column("updated_by", sa.String(length=255), nullable=True),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pipeline_name"),
    )
    op.create_index(op.f("ix_pipeline_id"), "pipeline", ["id"], unique=False)

    # Create pipeline_version table
    op.create_table(
        "pipeline_version",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "INACTIVE", name="pipelineversionstatus"),
            nullable=False,
        ),
        sa.Column("created_by", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.Column("updated_by", sa.String(length=255), nullable=True),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pipeline_version_id"), "pipeline_version", ["id"], unique=False)

    # Create pipeline_step table
    op.create_table(
        "pipeline_step",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_version_id", sa.Integer(), nullable=False),
        sa.Column("step_name", sa.String(length=255), nullable=False),
        sa.Column("service_endpoint_url", sa.String(length=512), nullable=False),
        sa.Column("step_order", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.Column("updated_by", sa.String(length=255), nullable=True),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_version_id"],
            ["pipeline_version.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pipeline_step_id"), "pipeline_step", ["id"], unique=False)

    # Create subscription_filter table
    op.create_table(
        "subscription_filter",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("subscription_id", sa.Integer(), nullable=False),
        sa.Column("filter_name", sa.String(length=255), nullable=False),
        sa.Column("filter_attributes", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.Column("updated_by", sa.String(length=255), nullable=True),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["subscription_id"],
            ["subscription.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_subscription_filter_id"), "subscription_filter", ["id"], unique=False
    )

    # Create subscription_filter_pipeline junction table
    op.create_table(
        "subscription_filter_pipeline",
        sa.Column("subscription_filter_id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.id"],
        ),
        sa.ForeignKeyConstraint(
            ["subscription_filter_id"],
            ["subscription_filter.id"],
        ),
        sa.PrimaryKeyConstraint("subscription_filter_id", "pipeline_id"),
    )


def downgrade() -> None:
    op.drop_table("subscription_filter_pipeline")
    op.drop_index(op.f("ix_subscription_filter_id"), table_name="subscription_filter")
    op.drop_table("subscription_filter")
    op.drop_index(op.f("ix_pipeline_step_id"), table_name="pipeline_step")
    op.drop_table("pipeline_step")
    op.drop_index(op.f("ix_pipeline_version_id"), table_name="pipeline_version")
    op.drop_table("pipeline_version")
    op.drop_index(op.f("ix_pipeline_id"), table_name="pipeline")
    op.drop_table("pipeline")
    op.drop_index(op.f("ix_subscription_id"), table_name="subscription")
    op.drop_table("subscription")
    op.drop_index(op.f("ix_source_schema_source_system"), table_name="source_schema")
    op.drop_index(op.f("ix_source_schema_id"), table_name="source_schema")
    op.drop_table("source_schema")
