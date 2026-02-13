from sqlalchemy.orm import Session
from sqlalchemy import func

from src.pipeline.models import Pipeline, PipelineVersion, PipelineStep, PipelineVersionStatus
from src.pipeline.schemas import (
    PipelineCreate,
    PipelineUpdate,
    PipelineVersionCreate,
    PipelineVersionUpdate,
    PipelineStepCreate,
)


class PipelineRepository:
    """Data access layer for pipelines."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: PipelineCreate, user_id: str | None = None) -> Pipeline:
        """Create a new pipeline with optional initial version."""
        db_pipeline = Pipeline(
            pipeline_name=data.pipeline_name,
            description=data.description,
            connector_id=data.connector_id,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(db_pipeline)
        self.db.flush()

        # Create initial version if steps are provided
        if data.steps:
            self._create_version_with_steps(db_pipeline.id, 1, data.steps, user_id)

        self.db.commit()
        self.db.refresh(db_pipeline)
        return db_pipeline

    def get_by_id(self, pipeline_id: int) -> Pipeline | None:
        """Get a pipeline by ID with all versions."""
        return self.db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()

    def get_by_name(self, pipeline_name: str) -> Pipeline | None:
        """Get a pipeline by name."""
        return (
            self.db.query(Pipeline)
            .filter(Pipeline.pipeline_name == pipeline_name)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Pipeline]:
        """Get all pipelines with pagination."""
        return self.db.query(Pipeline).offset(skip).limit(limit).all()

    def update(
        self, pipeline_id: int, data: PipelineUpdate, user_id: str | None = None
    ) -> Pipeline | None:
        """Update a pipeline."""
        db_pipeline = self.get_by_id(pipeline_id)
        if not db_pipeline:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_pipeline, field, value)

        db_pipeline.updated_by = user_id
        self.db.commit()
        self.db.refresh(db_pipeline)
        return db_pipeline

    def delete(self, pipeline_id: int) -> bool:
        """Delete a pipeline and all its versions."""
        db_pipeline = self.get_by_id(pipeline_id)
        if not db_pipeline:
            return False
        self.db.delete(db_pipeline)
        self.db.commit()
        return True

    def create_version(
        self,
        pipeline_id: int,
        data: PipelineVersionCreate,
        user_id: str | None = None,
    ) -> PipelineVersion | None:
        """Create a new version for an existing pipeline."""
        pipeline = self.get_by_id(pipeline_id)
        if not pipeline:
            return None

        # Get the next version number
        max_version = (
            self.db.query(func.max(PipelineVersion.version))
            .filter(PipelineVersion.pipeline_id == pipeline_id)
            .scalar()
        ) or 0
        next_version = max_version + 1

        version = self._create_version_with_steps(
            pipeline_id, next_version, data.steps, user_id
        )
        self.db.commit()
        self.db.refresh(version)
        return version

    def get_version(
        self, pipeline_id: int, version_number: int
    ) -> PipelineVersion | None:
        """Get a specific version of a pipeline."""
        return (
            self.db.query(PipelineVersion)
            .filter(
                PipelineVersion.pipeline_id == pipeline_id,
                PipelineVersion.version == version_number,
            )
            .first()
        )

    def update_version(
        self,
        pipeline_id: int,
        version_number: int,
        data: PipelineVersionUpdate,
        user_id: str | None = None,
    ) -> PipelineVersion | None:
        """Update a pipeline version."""
        version = self.get_version(pipeline_id, version_number)
        if not version:
            return None

        # If activating this version, deactivate others
        if data.status == PipelineVersionStatus.ACTIVE:
            self._deactivate_all_versions(pipeline_id)

        if data.status is not None:
            version.status = data.status

        # Update steps if provided
        if data.steps is not None:
            # Remove existing steps
            for step in version.steps:
                self.db.delete(step)

            # Add new steps
            for step_data in data.steps:
                step = PipelineStep(
                    pipeline_version_id=version.id,
                    step_name=step_data.step_name,
                    service_endpoint_url=step_data.service_endpoint_url,
                    step_order=step_data.step_order,
                    created_by=user_id,
                    updated_by=user_id,
                )
                self.db.add(step)

        version.updated_by = user_id
        self.db.commit()
        self.db.refresh(version)
        return version

    def _create_version_with_steps(
        self,
        pipeline_id: int,
        version_number: int,
        steps: list[PipelineStepCreate],
        user_id: str | None = None,
    ) -> PipelineVersion:
        """Helper to create a version with steps."""
        version = PipelineVersion(
            pipeline_id=pipeline_id,
            version=version_number,
            status=PipelineVersionStatus.INACTIVE,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(version)
        self.db.flush()

        for step_data in steps:
            step = PipelineStep(
                pipeline_version_id=version.id,
                step_name=step_data.step_name,
                service_endpoint_url=step_data.service_endpoint_url,
                step_order=step_data.step_order,
                created_by=user_id,
                updated_by=user_id,
            )
            self.db.add(step)

        return version

    def _deactivate_all_versions(self, pipeline_id: int) -> None:
        """Deactivate all versions of a pipeline."""
        self.db.query(PipelineVersion).filter(
            PipelineVersion.pipeline_id == pipeline_id
        ).update({PipelineVersion.status: PipelineVersionStatus.INACTIVE})
