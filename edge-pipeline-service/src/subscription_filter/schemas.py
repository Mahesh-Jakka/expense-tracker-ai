from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict


class SubscriptionFilterBase(BaseModel):
    """Base schema for subscription filter data."""

    subscription_id: int
    filter_name: str
    filter_attributes: dict[str, Any]


class SubscriptionFilterCreate(SubscriptionFilterBase):
    """Schema for creating a subscription filter."""

    pass


class SubscriptionFilterUpdate(BaseModel):
    """Schema for updating a subscription filter."""

    filter_name: str | None = None
    filter_attributes: dict[str, Any] | None = None


class AttachPipelinesRequest(BaseModel):
    """Schema for attaching pipelines to a filter."""

    pipeline_ids: list[int]


class PipelineSummary(BaseModel):
    """Summary schema for attached pipelines."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    pipeline_name: str


class SubscriptionFilterResponse(SubscriptionFilterBase):
    """Schema for subscription filter response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    pipelines: list[PipelineSummary]
    created_by: str | None
    created_at: datetime
    updated_by: str | None
    updated_at: datetime
