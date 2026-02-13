from sqlalchemy.orm import Session

from src.pipeline.repository import PipelineRepository
from src.pipeline.schemas import (
    PipelineCreate,
    PipelineUpdate,
    PipelineResponse,
    PipelineListResponse,
    PipelineVersionCreate,
    PipelineVersionUpdate,
    PipelineVersionResponse,
)
from src.core.exceptions import NotFoundError, ConflictError


class PipelineService:
    """Business logic layer for pipelines."""

    def __init__(self, db: Session):
        self.repository = PipelineRepository(db)

    def create_pipeline(
        self, data: PipelineCreate, user_id: str | None = None
    ) -> PipelineResponse:
        """Create a new pipeline."""
        # Check for duplicate name
        existing = self.repository.get_by_name(data.pipeline_name)
        if existing:
            raise ConflictError(
                f"Pipeline with name '{data.pipeline_name}' already exists"
            )

        db_pipeline = self.repository.create(data, user_id)
        return PipelineResponse.model_validate(db_pipeline)

    def get_pipeline(self, pipeline_id: int) -> PipelineResponse:
        """Get a pipeline by ID with all versions."""
        db_pipeline = self.repository.get_by_id(pipeline_id)
        if not db_pipeline:
            raise NotFoundError("Pipeline", pipeline_id)
        return PipelineResponse.model_validate(db_pipeline)

    def get_all_pipelines(
        self, skip: int = 0, limit: int = 100
    ) -> list[PipelineListResponse]:
        """Get all pipelines (without full version details)."""
        pipelines = self.repository.get_all(skip, limit)
        return [PipelineListResponse.model_validate(p) for p in pipelines]

    def update_pipeline(
        self, pipeline_id: int, data: PipelineUpdate, user_id: str | None = None
    ) -> PipelineResponse:
        """Update a pipeline."""
        # Check for duplicate name if being updated
        if data.pipeline_name:
            existing = self.repository.get_by_name(data.pipeline_name)
            if existing and existing.id != pipeline_id:
                raise ConflictError(
                    f"Pipeline with name '{data.pipeline_name}' already exists"
                )

        db_pipeline = self.repository.update(pipeline_id, data, user_id)
        if not db_pipeline:
            raise NotFoundError("Pipeline", pipeline_id)
        return PipelineResponse.model_validate(db_pipeline)

    def create_version(
        self,
        pipeline_id: int,
        data: PipelineVersionCreate,
        user_id: str | None = None,
    ) -> PipelineVersionResponse:
        """Create a new version for a pipeline."""
        version = self.repository.create_version(pipeline_id, data, user_id)
        if not version:
            raise NotFoundError("Pipeline", pipeline_id)
        return PipelineVersionResponse.model_validate(version)

    def get_version(
        self, pipeline_id: int, version_number: int
    ) -> PipelineVersionResponse:
        """Get a specific version of a pipeline."""
        version = self.repository.get_version(pipeline_id, version_number)
        if not version:
            raise NotFoundError(
                "PipelineVersion", f"pipeline_id={pipeline_id}, version={version_number}"
            )
        return PipelineVersionResponse.model_validate(version)

    def update_version(
        self,
        pipeline_id: int,
        version_number: int,
        data: PipelineVersionUpdate,
        user_id: str | None = None,
    ) -> PipelineVersionResponse:
        """Update a pipeline version (e.g., activate/deactivate, update steps)."""
        version = self.repository.update_version(
            pipeline_id, version_number, data, user_id
        )
        if not version:
            raise NotFoundError(
                "PipelineVersion", f"pipeline_id={pipeline_id}, version={version_number}"
            )
        return PipelineVersionResponse.model_validate(version)
