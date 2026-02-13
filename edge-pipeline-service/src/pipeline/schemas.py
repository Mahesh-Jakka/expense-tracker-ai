from datetime import datetime
from pydantic import BaseModel, ConfigDict

from src.pipeline.models import PipelineVersionStatus


# Pipeline Step schemas
class PipelineStepBase(BaseModel):
    """Base schema for pipeline step data."""

    step_name: str
    service_endpoint_url: str
    step_order: int


class PipelineStepCreate(PipelineStepBase):
    """Schema for creating a pipeline step."""

    pass


class PipelineStepResponse(PipelineStepBase):
    """Schema for pipeline step response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    pipeline_version_id: int


# Pipeline Version schemas
class PipelineVersionBase(BaseModel):
    """Base schema for pipeline version data."""

    status: PipelineVersionStatus = PipelineVersionStatus.INACTIVE


class PipelineVersionCreate(BaseModel):
    """Schema for creating a pipeline version."""

    steps: list[PipelineStepCreate]


class PipelineVersionUpdate(BaseModel):
    """Schema for updating a pipeline version."""

    status: PipelineVersionStatus | None = None
    steps: list[PipelineStepCreate] | None = None


class PipelineVersionResponse(BaseModel):
    """Schema for pipeline version response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    pipeline_id: int
    version: int
    status: PipelineVersionStatus
    steps: list[PipelineStepResponse]
    created_by: str | None
    created_at: datetime
    updated_by: str | None
    updated_at: datetime


# Pipeline schemas
class PipelineBase(BaseModel):
    """Base schema for pipeline data."""

    pipeline_name: str
    description: str | None = None
    connector_id: str | None = None


class PipelineCreate(PipelineBase):
    """Schema for creating a pipeline."""

    steps: list[PipelineStepCreate] | None = None


class PipelineUpdate(BaseModel):
    """Schema for updating a pipeline."""

    pipeline_name: str | None = None
    description: str | None = None
    connector_id: str | None = None


class PipelineResponse(PipelineBase):
    """Schema for pipeline response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    versions: list[PipelineVersionResponse]
    created_by: str | None
    created_at: datetime
    updated_by: str | None
    updated_at: datetime


class PipelineListResponse(PipelineBase):
    """Schema for pipeline list response (without full version details)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: str | None
    created_at: datetime
    updated_by: str | None
    updated_at: datetime
