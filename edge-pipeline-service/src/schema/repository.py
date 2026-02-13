from sqlalchemy.orm import Session

from src.schema.models import SourceSchema
from src.schema.schemas import SourceSchemaCreate, SourceSchemaUpdate


class SourceSchemaRepository:
    """Data access layer for source schemas."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SourceSchemaCreate, user_id: str | None = None) -> SourceSchema:
        """Create a new source schema."""
        db_schema = SourceSchema(
            source_system=data.source_system,
            source_schema=data.source_schema,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(db_schema)
        self.db.commit()
        self.db.refresh(db_schema)
        return db_schema

    def get_by_id(self, schema_id: int) -> SourceSchema | None:
        """Get a source schema by ID."""
        return self.db.query(SourceSchema).filter(SourceSchema.id == schema_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SourceSchema]:
        """Get all source schemas with pagination."""
        return self.db.query(SourceSchema).offset(skip).limit(limit).all()

    def update(
        self, schema_id: int, data: SourceSchemaUpdate, user_id: str | None = None
    ) -> SourceSchema | None:
        """Update a source schema."""
        db_schema = self.get_by_id(schema_id)
        if not db_schema:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_schema, field, value)

        db_schema.updated_by = user_id
        self.db.commit()
        self.db.refresh(db_schema)
        return db_schema

    def delete(self, schema_id: int) -> bool:
        """Delete a source schema."""
        db_schema = self.get_by_id(schema_id)
        if not db_schema:
            return False
        self.db.delete(db_schema)
        self.db.commit()
        return True
