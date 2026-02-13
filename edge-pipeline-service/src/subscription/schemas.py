from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SubscriptionBase(BaseModel):
    """Base schema for subscription data."""

    gcp_subscription_id: str
    subscription_name: str
    project_id: str
    topic_id: str


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a subscription."""

    pass


class SubscriptionUpdate(BaseModel):
    """Schema for updating a subscription."""

    gcp_subscription_id: str | None = None
    subscription_name: str | None = None
    project_id: str | None = None
    topic_id: str | None = None


class SubscriptionResponse(SubscriptionBase):
    """Schema for subscription response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: str | None
    created_at: datetime
    updated_by: str | None
    updated_at: datetime
