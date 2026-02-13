from sqlalchemy.orm import Session

from src.schema.repository import SourceSchemaRepository
from src.schema.schemas import SourceSchemaCreate, SourceSchemaUpdate, SourceSchemaResponse
from src.core.exceptions import NotFoundError


class SourceSchemaService:
    """Business logic layer for source schemas."""

    def __init__(self, db: Session):
        self.repository = SourceSchemaRepository(db)

    def create_schema(
        self, data: SourceSchemaCreate, user_id: str | None = None
    ) -> SourceSchemaResponse:
        """Create a new source schema."""
        db_schema = self.repository.create(data, user_id)
        return SourceSchemaResponse.model_validate(db_schema)

    def get_schema(self, schema_id: int) -> SourceSchemaResponse:
        """Get a source schema by ID."""
        db_schema = self.repository.get_by_id(schema_id)
        if not db_schema:
            raise NotFoundError("SourceSchema", schema_id)
        return SourceSchemaResponse.model_validate(db_schema)

    def get_all_schemas(
        self, skip: int = 0, limit: int = 100
    ) -> list[SourceSchemaResponse]:
        """Get all source schemas."""
        schemas = self.repository.get_all(skip, limit)
        return [SourceSchemaResponse.model_validate(s) for s in schemas]

    def update_schema(
        self, schema_id: int, data: SourceSchemaUpdate, user_id: str | None = None
    ) -> SourceSchemaResponse:
        """Update a source schema."""
        db_schema = self.repository.update(schema_id, data, user_id)
        if not db_schema:
            raise NotFoundError("SourceSchema", schema_id)
        return SourceSchemaResponse.model_validate(db_schema)

    def delete_schema(self, schema_id: int) -> None:
        """Delete a source schema."""
        if not self.repository.delete(schema_id):
            raise NotFoundError("SourceSchema", schema_id)
