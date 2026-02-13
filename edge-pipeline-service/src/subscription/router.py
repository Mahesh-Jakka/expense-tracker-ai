from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.dependencies import get_db, get_current_user
from src.subscription.service import SubscriptionService
from src.subscription.schemas import (
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionResponse,
)

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post(
    "", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED
)
def create_subscription(
    data: SubscriptionCreate,
    db: Session = Depends(get_db),
    user_id: str | None = Depends(get_current_user),
) -> SubscriptionResponse:
    """Create a new subscription."""
    service = SubscriptionService(db)
    return service.create_subscription(data, user_id)


@router.get("", response_model=list[SubscriptionResponse])
def get_subscriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[SubscriptionResponse]:
    """Get all subscriptions."""
    service = SubscriptionService(db)
    return service.get_all_subscriptions(skip, limit)


@router.get("/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
) -> SubscriptionResponse:
    """Get a subscription by ID."""
    service = SubscriptionService(db)
    return service.get_subscription(subscription_id)


@router.put("/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(
    subscription_id: int,
    data: SubscriptionUpdate,
    db: Session = Depends(get_db),
    user_id: str | None = Depends(get_current_user),
) -> SubscriptionResponse:
    """Update a subscription."""
    service = SubscriptionService(db)
    return service.update_subscription(subscription_id, data, user_id)
