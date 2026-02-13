from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.dependencies import get_db, get_current_user
from src.pipeline.service import PipelineService
from src.pipeline.schemas import (
    PipelineCreate,
    PipelineUpdate,
    PipelineResponse,
    PipelineListResponse,
    PipelineVersionCreate,
    PipelineVersionUpdate,
    PipelineVersionResponse,
)

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])


@router.post("", response_model=PipelineResponse, status_code=status.HTTP_201_CREATED)
def create_pipeline(
    data: PipelineCreate,
    db: Session = Depends(get_db),
    user_id: str | None = Depends(get_current_user),
) -> PipelineResponse:
    """Create a new pipeline with optional initial version."""
    service = PipelineService(db)
    return service.create_pipeline(data, user_id)


@router.get("", response_model=list[PipelineListResponse])
def get_pipelines(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[PipelineListResponse]:
    """Get all pipelines."""
    service = PipelineService(db)
    return service.get_all_pipelines(skip, limit)


@router.get("/{pipeline_id}", response_model=PipelineResponse)
def get_pipeline(
    pipeline_id: int,
    db: Session = Depends(get_db),
) -> PipelineResponse:
    """Get a pipeline by ID with all versions."""
    service = PipelineService(db)
    return service.get_pipeline(pipeline_id)


@router.put("/{pipeline_id}", response_model=PipelineResponse)
def update_pipeline(
    pipeline_id: int,
    data: PipelineUpdate,
    db: Session = Depends(get_db),
    user_id: str | None = Depends(get_current_user),
) -> PipelineResponse:
    """Update a pipeline."""
    service = PipelineService(db)
    return service.update_pipeline(pipeline_id, data, user_id)


@router.post(
    "/{pipeline_id}",
    response_model=PipelineVersionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_version(
    pipeline_id: int,
    data: PipelineVersionCreate,
    db: Session = Depends(get_db),
    user_id: str | None = Depends(get_current_user),
) -> PipelineVersionResponse:
    """Create a new version for a pipeline."""
    service = PipelineService(db)
    return service.create_version(pipeline_id, data, user_id)


@router.get(
    "/{pipeline_id}/version/{version_number}", response_model=PipelineVersionResponse
)
def get_version(
    pipeline_id: int,
    version_number: int,
    db: Session = Depends(get_db),
) -> PipelineVersionResponse:
    """Get a specific version of a pipeline."""
    service = PipelineService(db)
    return service.get_version(pipeline_id, version_number)


@router.put(
    "/{pipeline_id}/version/{version_number}", response_model=PipelineVersionResponse
)
def update_version(
    pipeline_id: int,
    version_number: int,
    data: PipelineVersionUpdate,
    db: Session = Depends(get_db),
    user_id: str | None = Depends(get_current_user),
) -> PipelineVersionResponse:
    """Update a pipeline version (activate/deactivate, update steps)."""
    service = PipelineService(db)
    return service.update_version(pipeline_id, version_number, data, user_id)
