from fastapi import status

from app.core.base_test import BaseTest


class TestJoseAuth(BaseTest):
    def test_create_user_unauthorized(self):
        response = self.client.post("jose_auth/create_user")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_auth_user(self, db_session):
        response = self.get_login_headers("jose_auth/token")
        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert "access_token" in json_response
        assert "token_type" in json_response
