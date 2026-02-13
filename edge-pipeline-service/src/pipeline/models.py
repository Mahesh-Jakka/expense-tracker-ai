from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
import enum

from src.database import Base
from src.core.base_models import AuditMixin


class PipelineVersionStatus(str, enum.Enum):
    """Status of a pipeline version."""

    ACTIVE = "active"
    INACTIVE = "inactive"


class Pipeline(AuditMixin, Base):
    """SQLAlchemy model for pipelines."""

    __tablename__ = "pipeline"

    pipeline_name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    connector_id = Column(String(255), nullable=True)

    # Relationship to versions
    versions = relationship(
        "PipelineVersion", back_populates="pipeline", cascade="all, delete-orphan"
    )


class PipelineVersion(AuditMixin, Base):
    """SQLAlchemy model for pipeline versions."""

    __tablename__ = "pipeline_version"

    pipeline_id = Column(Integer, ForeignKey("pipeline.id"), nullable=False)
    version = Column(Integer, nullable=False)
    status = Column(
        Enum(PipelineVersionStatus),
        default=PipelineVersionStatus.INACTIVE,
        nullable=False,
    )

    # Relationships
    pipeline = relationship("Pipeline", back_populates="versions")
    steps = relationship(
        "PipelineStep", back_populates="pipeline_version", cascade="all, delete-orphan"
    )


class PipelineStep(AuditMixin, Base):
    """SQLAlchemy model for pipeline steps."""

    __tablename__ = "pipeline_step"

    pipeline_version_id = Column(
        Integer, ForeignKey("pipeline_version.id"), nullable=False
    )
    step_name = Column(String(255), nullable=False)
    service_endpoint_url = Column(String(512), nullable=False)
    step_order = Column(Integer, nullable=False)

    # Relationship
    pipeline_version = relationship("PipelineVersion", back_populates="steps")
