from collections.abc import Generator

import pytest
import redis
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlmodel import Session, SQLModel

from app.core.database import create_engine, init_db, settings
from app.main import app
from app.tests.init_factories import init_factories


@pytest.fixture(scope="session", autouse=True)
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(settings.TEST_SQLALCHEMY_DATABASE_URI)
    try:
        # Configure Alembic
        alembic_cfg = Config(f"{settings.PROJECT_PATH}/alembic.ini")
        alembic_cfg.set_main_option(
            "sqlalchemy.url", settings.TEST_SQLALCHEMY_DATABASE_URI
        )
        # Run all migrations
        command.upgrade(alembic_cfg, "head")
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            init_factories(session)
            init_db(session)
            yield session
            session.rollback()
            session.close()
    finally:
        SQLModel.metadata.drop_all(engine)
        ...


@pytest.fixture(scope="session")
def initialize_cache():
    redis_connection = redis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis_connection), prefix="fastapi-cache")
    yield
    FastAPICache.clear()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
