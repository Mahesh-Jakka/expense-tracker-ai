from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.dependencies import get_db, get_current_user
from src.subscription_filter.service import SubscriptionFilterService
from src.subscription_filter.schemas import (
    SubscriptionFilterCreate,
    SubscriptionFilterUpdate,
    SubscriptionFilterResponse,
    AttachPipelinesRequest,
)

router = APIRouter(prefix="/subscription_filter", tags=["Subscription Filter"])


@router.post(
    "", response_model=SubscriptionFilterResponse, status_code=status.HTTP_201_CREATED
)
def create_filter(
    data: SubscriptionFilterCreate,
    db: Session = Depends(get_db),
    user_id: str | None = Depends(get_current_user),
) -> SubscriptionFilterResponse:
    """Create a new subscription filter."""
    service = SubscriptionFilterService(db)
    return service.create_filter(data, user_id)


@router.get("", response_model=list[SubscriptionFilterResponse])
def get_filters(
    skip: int = 0,
    limit: int = 100,
    subscription_id: int | None = None,
    db: Session = Depends(get_db),
) -> list[SubscriptionFilterResponse]:
    """Get all subscription filters, optionally filtered by subscription."""
    service = SubscriptionFilterService(db)
    if subscription_id is not None:
        return service.get_filters_by_subscription(subscription_id, skip, limit)
    return service.get_all_filters(skip, limit)


@router.get("/{filter_id}", response_model=SubscriptionFilterResponse)
def get_filter(
    filter_id: int,
    db: Session = Depends(get_db),
) -> SubscriptionFilterResponse:
    """Get a subscription filter by ID."""
    service = SubscriptionFilterService(db)
    return service.get_filter(filter_id)


@router.put("/{filter_id}", response_model=SubscriptionFilterResponse)
def update_filter(
    filter_id: int,
    data: SubscriptionFilterUpdate,
    db: Session = Depends(get_db),
    user_id: str | None = Depends(get_current_user),
) -> SubscriptionFilterResponse:
    """Update a subscription filter."""
    service = SubscriptionFilterService(db)
    return service.update_filter(filter_id, data, user_id)


@router.put("/{filter_id}/attach", response_model=SubscriptionFilterResponse)
def attach_pipelines(
    filter_id: int,
    data: AttachPipelinesRequest,
    db: Session = Depends(get_db),
    user_id: str | None = Depends(get_current_user),
) -> SubscriptionFilterResponse:
    """Attach pipelines to a subscription filter."""
    service = SubscriptionFilterService(db)
    return service.attach_pipelines(filter_id, data, user_id)
