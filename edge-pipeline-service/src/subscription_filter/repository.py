from sqlalchemy.orm import Session

from src.subscription_filter.models import SubscriptionFilter
from src.subscription_filter.schemas import SubscriptionFilterCreate, SubscriptionFilterUpdate
from src.pipeline.models import Pipeline


class SubscriptionFilterRepository:
    """Data access layer for subscription filters."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self, data: SubscriptionFilterCreate, user_id: str | None = None
    ) -> SubscriptionFilter:
        """Create a new subscription filter."""
        db_filter = SubscriptionFilter(
            subscription_id=data.subscription_id,
            filter_name=data.filter_name,
            filter_attributes=data.filter_attributes,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(db_filter)
        self.db.commit()
        self.db.refresh(db_filter)
        return db_filter

    def get_by_id(self, filter_id: int) -> SubscriptionFilter | None:
        """Get a subscription filter by ID."""
        return (
            self.db.query(SubscriptionFilter)
            .filter(SubscriptionFilter.id == filter_id)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SubscriptionFilter]:
        """Get all subscription filters with pagination."""
        return self.db.query(SubscriptionFilter).offset(skip).limit(limit).all()

    def get_by_subscription(
        self, subscription_id: int, skip: int = 0, limit: int = 100
    ) -> list[SubscriptionFilter]:
        """Get all filters for a subscription."""
        return (
            self.db.query(SubscriptionFilter)
            .filter(SubscriptionFilter.subscription_id == subscription_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        filter_id: int,
        data: SubscriptionFilterUpdate,
        user_id: str | None = None,
    ) -> SubscriptionFilter | None:
        """Update a subscription filter."""
        db_filter = self.get_by_id(filter_id)
        if not db_filter:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_filter, field, value)

        db_filter.updated_by = user_id
        self.db.commit()
        self.db.refresh(db_filter)
        return db_filter

    def delete(self, filter_id: int) -> bool:
        """Delete a subscription filter."""
        db_filter = self.get_by_id(filter_id)
        if not db_filter:
            return False
        self.db.delete(db_filter)
        self.db.commit()
        return True

    def attach_pipelines(
        self,
        filter_id: int,
        pipeline_ids: list[int],
        user_id: str | None = None,
    ) -> SubscriptionFilter | None:
        """Attach pipelines to a subscription filter."""
        db_filter = self.get_by_id(filter_id)
        if not db_filter:
            return None

        # Get pipelines
        pipelines = (
            self.db.query(Pipeline).filter(Pipeline.id.in_(pipeline_ids)).all()
        )

        # Replace existing pipelines
        db_filter.pipelines = pipelines
        db_filter.updated_by = user_id
        self.db.commit()
        self.db.refresh(db_filter)
        return db_filter

    def get_pipeline_ids(self, filter_id: int) -> list[int]:
        """Get IDs of pipelines attached to a filter."""
        db_filter = self.get_by_id(filter_id)
        if not db_filter:
            return []
        return [p.id for p in db_filter.pipelines]
