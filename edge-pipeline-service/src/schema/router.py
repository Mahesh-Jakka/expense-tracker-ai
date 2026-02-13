from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.dependencies import get_db, get_current_user
from src.schema.service import SourceSchemaService
from src.schema.schemas import SourceSchemaCreate, SourceSchemaUpdate, SourceSchemaResponse

router = APIRouter(prefix="/schema", tags=["Schema"])


@router.post("", response_model=SourceSchemaResponse, status_code=status.HTTP_201_CREATED)
def create_schema(
    data: SourceSchemaCreate,
    db: Session = Depends(get_db),
    user_id: str | None = Depends(get_current_user),
) -> SourceSchemaResponse:
    """Create a new source schema."""
    service = SourceSchemaService(db)
    return service.create_schema(data, user_id)


@router.get("", response_model=list[SourceSchemaResponse])
def get_schemas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[SourceSchemaResponse]:
    """Get all source schemas."""
    service = SourceSchemaService(db)
    return service.get_all_schemas(skip, limit)


@router.get("/{schema_id}", response_model=SourceSchemaResponse)
def get_schema(
    schema_id: int,
    db: Session = Depends(get_db),
) -> SourceSchemaResponse:
    """Get a source schema by ID."""
    service = SourceSchemaService(db)
    return service.get_schema(schema_id)


@router.put("/{schema_id}", response_model=SourceSchemaResponse)
def update_schema(
    schema_id: int,
    data: SourceSchemaUpdate,
    db: Session = Depends(get_db),
    user_id: str | None = Depends(get_current_user),
) -> SourceSchemaResponse:
    """Update a source schema."""
    service = SourceSchemaService(db)
    return service.update_schema(schema_id, data, user_id)
