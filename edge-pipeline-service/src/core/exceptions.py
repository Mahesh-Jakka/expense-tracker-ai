from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    """Base exception for API errors."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "An unexpected error occurred",
    ):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundError(BaseAPIException):
    """Raised when a resource is not found."""

    def __init__(self, resource: str, identifier: int | str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id '{identifier}' not found",
        )


class ConflictError(BaseAPIException):
    """Raised when there's a conflict with existing data."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class ValidationError(BaseAPIException):
    """Raised when validation fails."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=422,
            detail=detail,
        )
