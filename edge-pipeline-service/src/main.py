from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.core.exceptions import BaseAPIException
from src.schema.router import router as schema_router
from src.subscription.router import router as subscription_router
from src.pipeline.router import router as pipeline_router
from src.subscription_filter.router import router as subscription_filter_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Edge Pipeline Service - Metadata Layer API",
    version="0.1.0",
)


@app.exception_handler(BaseAPIException)
async def api_exception_handler(request: Request, exc: BaseAPIException):
    """Handle custom API exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include routers
app.include_router(schema_router)
app.include_router(subscription_router)
app.include_router(pipeline_router)
app.include_router(subscription_filter_router)
