from fastapi.testclient import TestClient
from loguru import logger

from apps.authentication.tests.test_factories.test_user import UserFactory
from database import db_dependency
from main import app
from settings import EMAIL_TEST, PASSWORD_TEST, USERNAME_TEST


# Override the get_db dependency to use the test database
def override_get_db(db_session):
    yield from db_session

app.dependency_overrides[db_dependency] = override_get_db

class BaseTest:
    client = TestClient(app)
    client.headers["Content-Type"] = "application/json"
    user = None

    def create_user(self):
        self.user = UserFactory.create(
            username=USERNAME_TEST,
            email=EMAIL_TEST,
            hashed_password=PASSWORD_TEST
        )
        return self.user

    def get_login_headers(self, url):
        try:
            self.create_user()
        except Exception as error:
            logger.error(error)
        data = {"username": EMAIL_TEST, "password": PASSWORD_TEST}
        return self.client.post(url, json=data)
