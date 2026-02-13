from sqlalchemy import Column, String, JSON

from src.database import Base
from src.core.base_models import AuditMixin


class SourceSchema(AuditMixin, Base):
    """SQLAlchemy model for source schemas."""

    __tablename__ = "source_schema"

    source_system = Column(String(255), nullable=False, index=True)
    source_schema = Column(JSON, nullable=False)
