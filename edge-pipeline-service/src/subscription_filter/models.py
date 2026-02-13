from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship

from src.database import Base
from src.core.base_models import AuditMixin


# Junction table for many-to-many relationship between SubscriptionFilter and Pipeline
subscription_filter_pipeline = Table(
    "subscription_filter_pipeline",
    Base.metadata,
    Column(
        "subscription_filter_id",
        Integer,
        ForeignKey("subscription_filter.id"),
        primary_key=True,
    ),
    Column("pipeline_id", Integer, ForeignKey("pipeline.id"), primary_key=True),
)


class SubscriptionFilter(AuditMixin, Base):
    """SQLAlchemy model for subscription filters."""

    __tablename__ = "subscription_filter"

    subscription_id = Column(Integer, ForeignKey("subscription.id"), nullable=False)
    filter_name = Column(String(255), nullable=False)
    filter_attributes = Column(JSON, nullable=False)

    # Relationships
    subscription = relationship("Subscription", back_populates="filters")
    pipelines = relationship(
        "Pipeline",
        secondary=subscription_filter_pipeline,
        backref="subscription_filters",
    )
