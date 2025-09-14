from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import redis
import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import app_metadata, settings
from app.core.logger import setup_logger

logger = setup_logger(__name__, level=settings.log_level_number)


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "dev":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)


openapi_prefix = settings.API_GATEWAY_PATH if settings.ACTIVE_API_GATEWAY else ""
logger.info(f"OpenAPI prefix: {openapi_prefix}")




@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    print("---> lifespan start")
    logger.info("---> lifespan start")
    redis_connection = redis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis_connection), prefix="fastapi-cache")
    yield
    print("---> lifespan finish")
    logger.info("---> lifespan finish")


app = FastAPI(
    title=app_metadata.project_name,
    description=app_metadata.project_description,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version=app_metadata.project_version,
    generate_unique_id_function=custom_generate_unique_id,
    docs_url="/docs",
    root_path=openapi_prefix,
    lifespan=lifespan,
)
headers = Mangum(app)


# Set all CORS enabled origins
if settings.ALLOWED_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
