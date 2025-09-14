import os

import tomllib
from pydantic import BaseModel

from app.core.logger import setup_logger

logger = setup_logger(__name__)
PROJECT_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
PYPROJECT_PATH = "/".join((PROJECT_PATH, "pyproject.toml"))


class ProjectMetadata(BaseModel):
    project_name: str
    project_version: str
    project_description: str


def read_project_metadata() -> ProjectMetadata:
    with open(PYPROJECT_PATH, "rb") as f:
        data = tomllib.load(f)
    project = data.get("project", {})

    project_metadata = ProjectMetadata(
        project_name=project.get("name", ""),
        project_version=project.get("version", ""),
        project_description=project.get("description", ""),
    )

    logger.debug(f"Project Metadata: \n{project_metadata.model_dump_json(indent=4)}")

    return project_metadata
