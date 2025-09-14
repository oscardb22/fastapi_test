from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import app_metadata

router = APIRouter(tags=["general"])


class HealthResponse(BaseModel):
    status: str


class VersionResponse(BaseModel):
    version: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Standard health check endpoint for the service.
    """
    return HealthResponse(status="ok")


@router.get("/version", response_model=VersionResponse)
async def get_version():
    """
    Returns the current version of the project
    """
    return VersionResponse(version=app_metadata.project_version)
