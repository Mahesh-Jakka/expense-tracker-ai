from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict


class SourceSchemaBase(BaseModel):
    """Base schema for source schema data."""

    source_system: str
    source_schema: dict[str, Any]


class SourceSchemaCreate(SourceSchemaBase):
    """Schema for creating a source schema."""

    pass


class SourceSchemaUpdate(BaseModel):
    """Schema for updating a source schema."""

    source_system: str | None = None
    source_schema: dict[str, Any] | None = None


class SourceSchemaResponse(SourceSchemaBase):
    """Schema for source schema response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: str | None
    created_at: datetime
    updated_by: str | None
    updated_at: datetime
