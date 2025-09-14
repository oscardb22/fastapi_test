import logging
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, Field
from pydantic_settings import BaseSettings

from app.core.logger import setup_logger
from app.core.pyproject_reader import PROJECT_PATH, read_project_metadata

logger = setup_logger(__name__)

DEV_ENVIRONMENT = "dev"
PROD_ENVIRONMENT = "prod"


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    APP_NAME: str = Field(default="", env="APP_NAME")
    AWS_ACCESS_KEY_ID: str = Field(default="", env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(default="", env="AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET: str = Field(default="", env="AWS_S3_BUCKET")
    AWS_S3_REGION: str = Field(default="", env="AWS_S3_REGION")
    SENTRY_DSN: str = Field(default="", env="SENTRY_DSN")
    APP_ENV: Literal[DEV_ENVIRONMENT, PROD_ENVIRONMENT] = Field(
        default="", env="APP_ENV"
    )
    FIRST_SUPERUSER_USERNAME: str = Field(default="", env="FIRST_SUPERUSER_USERNAME")
    FIRST_SUPERUSER_EMAIL: str = Field(default="", env="FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = Field(default="", env="FIRST_SUPERUSER_PASSWORD")
    ALLOWED_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        Field(default="http://localhost", env="ALLOWED_CORS_ORIGINS")
    )
    ACTIVE_API_GATEWAY: bool = Field(default=True, env="ACTIVE_API_GATEWAY")
    API_GATEWAY_PATH: str = Field(default="/template", env="API_GATEWAY_PATH")
    SQLALCHEMY_DATABASE_URI: str = Field(default="", env="SQLALCHEMY_DATABASE_URI")
    TEST_SQLALCHEMY_DATABASE_URI: str = Field(
        default="", env="TEST_SQLALCHEMY_DATABASE_URI"
    )
    PROD_SQLALCHEMY_DATABASE_URI: str = Field(
        default="", env="PROD_SQLALCHEMY_DATABASE_URI"
    )
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", env="LOG_LEVEL"
    )
    VERSION: str = Field(default="", env="VERSION")
    SECRET_KEY: str = Field(default="", env="SECRET_KEY")
    ALGORITHM: str = Field(default="", env="ALGORITHM")
    TOKEN_TYPE: str = Field(default="", env="TOKEN_TYPE")
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    URL_CHAT_OPEN_AI: str = Field(default="", env="URL_CHAT_OPEN_AI")
    REDIS_URL: str = Field(default="", env="REDIS_URL")
    LANGUAGE_CODE: str = Field(default="", env="LANGUAGE_CODE")
    PROJECT_PATH: str = PROJECT_PATH
    API_V1_STR: str = Field(default="/api/v1", env="API_V1_STR")

    @property
    def log_level_number(self) -> int:
        mapping = logging.getLevelNamesMapping()
        return mapping.get(self.LOG_LEVEL, logging.INFO)

    class Config:
        env_file = f"{PROJECT_PATH}/vars.dev.env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields in the environment
        env_file_encoding = "utf-8"
        env_ignore_empty = True


settings = Settings()
app_metadata = read_project_metadata()
logger.debug(f"App Metadata: \n{app_metadata.model_dump_json(indent=4)}")
