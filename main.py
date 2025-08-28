from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from loguru import logger
from mangum import Mangum

from apps.api_ai.routes import open_ai
from apps.authentication.routes import jose_auth, py_jwt_auth
from settings import REDIS_URL


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    print("---> lifespan start")
    logger.info("---> lifespan start")
    redis_connection = redis.from_url(REDIS_URL)
    FastAPICache.init(RedisBackend(redis_connection), prefix="fastapi-cache")
    yield
    print("---> lifespan finish")
    logger.info("---> lifespan finish")


app = FastAPI(lifespan=lifespan)
app.include_router(jose_auth.router)
app.include_router(py_jwt_auth.router)
app.include_router(open_ai.router)
headers = Mangum(app)


@app.get("/")
@cache(expire=60)
async def index():
    return {"response": "my test"}
