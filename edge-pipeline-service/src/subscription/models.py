from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.database import Base
from src.core.base_models import AuditMixin


class Subscription(AuditMixin, Base):
    """SQLAlchemy model for subscriptions."""

    __tablename__ = "subscription"

    gcp_subscription_id = Column(String(255), nullable=False, unique=True)
    subscription_name = Column(String(255), nullable=False)
    project_id = Column(String(255), nullable=False)
    topic_id = Column(String(255), nullable=False)

    # Relationship to subscription filters
    filters = relationship(
        "SubscriptionFilter", back_populates="subscription", cascade="all, delete-orphan"
    )
