from sqlalchemy.orm import Session

from src.subscription_filter.repository import SubscriptionFilterRepository
from src.subscription_filter.schemas import (
    SubscriptionFilterCreate,
    SubscriptionFilterUpdate,
    SubscriptionFilterResponse,
    AttachPipelinesRequest,
)
from src.subscription.repository import SubscriptionRepository
from src.pipeline.repository import PipelineRepository
from src.core.exceptions import NotFoundError, ValidationError


class SubscriptionFilterService:
    """Business logic layer for subscription filters."""

    def __init__(self, db: Session):
        self.repository = SubscriptionFilterRepository(db)
        self.subscription_repo = SubscriptionRepository(db)
        self.pipeline_repo = PipelineRepository(db)

    def create_filter(
        self, data: SubscriptionFilterCreate, user_id: str | None = None
    ) -> SubscriptionFilterResponse:
        """Create a new subscription filter."""
        # Verify subscription exists
        subscription = self.subscription_repo.get_by_id(data.subscription_id)
        if not subscription:
            raise NotFoundError("Subscription", data.subscription_id)

        db_filter = self.repository.create(data, user_id)
        return SubscriptionFilterResponse.model_validate(db_filter)

    def get_filter(self, filter_id: int) -> SubscriptionFilterResponse:
        """Get a subscription filter by ID."""
        db_filter = self.repository.get_by_id(filter_id)
        if not db_filter:
            raise NotFoundError("SubscriptionFilter", filter_id)
        return SubscriptionFilterResponse.model_validate(db_filter)

    def get_all_filters(
        self, skip: int = 0, limit: int = 100
    ) -> list[SubscriptionFilterResponse]:
        """Get all subscription filters."""
        filters = self.repository.get_all(skip, limit)
        return [SubscriptionFilterResponse.model_validate(f) for f in filters]

    def get_filters_by_subscription(
        self, subscription_id: int, skip: int = 0, limit: int = 100
    ) -> list[SubscriptionFilterResponse]:
        """Get all filters for a subscription."""
        # Verify subscription exists
        subscription = self.subscription_repo.get_by_id(subscription_id)
        if not subscription:
            raise NotFoundError("Subscription", subscription_id)

        filters = self.repository.get_by_subscription(subscription_id, skip, limit)
        return [SubscriptionFilterResponse.model_validate(f) for f in filters]

    def update_filter(
        self,
        filter_id: int,
        data: SubscriptionFilterUpdate,
        user_id: str | None = None,
    ) -> SubscriptionFilterResponse:
        """Update a subscription filter."""
        db_filter = self.repository.update(filter_id, data, user_id)
        if not db_filter:
            raise NotFoundError("SubscriptionFilter", filter_id)
        return SubscriptionFilterResponse.model_validate(db_filter)

    def delete_filter(self, filter_id: int) -> None:
        """Delete a subscription filter."""
        if not self.repository.delete(filter_id):
            raise NotFoundError("SubscriptionFilter", filter_id)

    def attach_pipelines(
        self,
        filter_id: int,
        data: AttachPipelinesRequest,
        user_id: str | None = None,
    ) -> SubscriptionFilterResponse:
        """Attach pipelines to a subscription filter."""
        # Verify all pipelines exist
        for pipeline_id in data.pipeline_ids:
            pipeline = self.pipeline_repo.get_by_id(pipeline_id)
            if not pipeline:
                raise ValidationError(f"Pipeline with ID {pipeline_id} not found")

        db_filter = self.repository.attach_pipelines(
            filter_id, data.pipeline_ids, user_id
        )
        if not db_filter:
            raise NotFoundError("SubscriptionFilter", filter_id)
        return SubscriptionFilterResponse.model_validate(db_filter)
