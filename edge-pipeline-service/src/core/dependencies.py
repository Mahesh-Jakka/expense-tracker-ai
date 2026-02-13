from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, Header

from src.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(x_user_id: str | None = Header(default=None)) -> str | None:
    """
    Placeholder for authentication.
    In production, this would validate tokens and return user info.
    For now, it reads user ID from a header for audit purposes.
    """
    return x_user_id
