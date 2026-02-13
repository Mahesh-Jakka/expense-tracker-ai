from sqlalchemy.orm import Session

from src.subscription.models import Subscription
from src.subscription.schemas import SubscriptionCreate, SubscriptionUpdate


class SubscriptionRepository:
    """Data access layer for subscriptions."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SubscriptionCreate, user_id: str | None = None) -> Subscription:
        """Create a new subscription."""
        db_subscription = Subscription(
            gcp_subscription_id=data.gcp_subscription_id,
            subscription_name=data.subscription_name,
            project_id=data.project_id,
            topic_id=data.topic_id,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(db_subscription)
        self.db.commit()
        self.db.refresh(db_subscription)
        return db_subscription

    def get_by_id(self, subscription_id: int) -> Subscription | None:
        """Get a subscription by ID."""
        return (
            self.db.query(Subscription)
            .filter(Subscription.id == subscription_id)
            .first()
        )

    def get_by_gcp_id(self, gcp_subscription_id: str) -> Subscription | None:
        """Get a subscription by GCP subscription ID."""
        return (
            self.db.query(Subscription)
            .filter(Subscription.gcp_subscription_id == gcp_subscription_id)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Subscription]:
        """Get all subscriptions with pagination."""
        return self.db.query(Subscription).offset(skip).limit(limit).all()

    def update(
        self, subscription_id: int, data: SubscriptionUpdate, user_id: str | None = None
    ) -> Subscription | None:
        """Update a subscription."""
        db_subscription = self.get_by_id(subscription_id)
        if not db_subscription:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_subscription, field, value)

        db_subscription.updated_by = user_id
        self.db.commit()
        self.db.refresh(db_subscription)
        return db_subscription

    def delete(self, subscription_id: int) -> bool:
        """Delete a subscription."""
        db_subscription = self.get_by_id(subscription_id)
        if not db_subscription:
            return False
        self.db.delete(db_subscription)
        self.db.commit()
        return True
