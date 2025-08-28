import pytest
import redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apps.authentication.tests.test_factories.test_user import UserFactory
from database import Base
from settings import REDIS_URL, TEST_SQLALCHEMY_DATABASE_URL


@pytest.fixture(scope="function", autouse=True)
def db_session():
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    UserFactory._meta.sqlalchemy_session = session # Link factory to session
    yield session
    session.rollback() # Rollback changes after each test
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def initialize_cache():
    redis_connection = redis.from_url(REDIS_URL)
    FastAPICache.init(RedisBackend(redis_connection), prefix="fastapi-cache")
    yield
    FastAPICache.clear()
