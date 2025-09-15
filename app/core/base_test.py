from fastapi.testclient import TestClient
from loguru import logger

from app.core.config import settings
from app.main import app
from app.tests.test_factories.test_user import UserFactory


# Override the get_db dependency to use the test database
def override_get_db(db_session):
    yield from db_session


class BaseTest(TestClient):
    user = None
    def __init__(self):
        super().__init__(app=app)
        self.client.headers["Content-Type"] = "application/json"
        self.base_url = f"{self.base_url}{settings.API_V1_STR}/"

    def create_user(self):
        self.user = UserFactory.create(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=settings.FIRST_SUPERUSER_PASSWORD
        )
        return self.user

    def get_login_headers(self, url):
        try:
            self.create_user()
        except Exception as error:
            logger.error(f"[{url}] - {error}")
        data = {"username": settings.FIRST_SUPERUSER_EMAIL, "password": settings.FIRST_SUPERUSER_PASSWORD}
        return self.client.post(
            url,
            data=data,
            headers={
                "Content-Type":"application/x-www-form-urlencoded",
                "accept": "application/json, text/plain, */*"
            }
        )
