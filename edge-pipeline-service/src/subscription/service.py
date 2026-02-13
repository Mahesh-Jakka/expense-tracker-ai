from sqlalchemy.orm import Session

from src.subscription.repository import SubscriptionRepository
from src.subscription.schemas import (
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionResponse,
)
from src.core.exceptions import NotFoundError, ConflictError


class SubscriptionService:
    """Business logic layer for subscriptions."""

    def __init__(self, db: Session):
        self.repository = SubscriptionRepository(db)

    def create_subscription(
        self, data: SubscriptionCreate, user_id: str | None = None
    ) -> SubscriptionResponse:
        """Create a new subscription."""
        # Check for duplicate GCP subscription ID
        existing = self.repository.get_by_gcp_id(data.gcp_subscription_id)
        if existing:
            raise ConflictError(
                f"Subscription with GCP ID '{data.gcp_subscription_id}' already exists"
            )

        db_subscription = self.repository.create(data, user_id)
        return SubscriptionResponse.model_validate(db_subscription)

    def get_subscription(self, subscription_id: int) -> SubscriptionResponse:
        """Get a subscription by ID."""
        db_subscription = self.repository.get_by_id(subscription_id)
        if not db_subscription:
            raise NotFoundError("Subscription", subscription_id)
        return SubscriptionResponse.model_validate(db_subscription)

    def get_all_subscriptions(
        self, skip: int = 0, limit: int = 100
    ) -> list[SubscriptionResponse]:
        """Get all subscriptions."""
        subscriptions = self.repository.get_all(skip, limit)
        return [SubscriptionResponse.model_validate(s) for s in subscriptions]

    def update_subscription(
        self, subscription_id: int, data: SubscriptionUpdate, user_id: str | None = None
    ) -> SubscriptionResponse:
        """Update a subscription."""
        # Check for duplicate GCP subscription ID if being updated
        if data.gcp_subscription_id:
            existing = self.repository.get_by_gcp_id(data.gcp_subscription_id)
            if existing and existing.id != subscription_id:
                raise ConflictError(
                    f"Subscription with GCP ID '{data.gcp_subscription_id}' already exists"
                )

        db_subscription = self.repository.update(subscription_id, data, user_id)
        if not db_subscription:
            raise NotFoundError("Subscription", subscription_id)
        return SubscriptionResponse.model_validate(db_subscription)

    def delete_subscription(self, subscription_id: int) -> None:
        """Delete a subscription."""
        if not self.repository.delete(subscription_id):
            raise NotFoundError("Subscription", subscription_id)
