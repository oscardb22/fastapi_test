from fastapi import status

from base_test import BaseTest


class TestPyJwt(BaseTest):
    def test_create_user_unauthorized(self):
        response = self.client.post("/py_jwt_auth/create_user")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_auth_user(self, db_session):
        response = self.get_login_headers("/py_jwt_auth/token")
        json_response = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in json_response
        assert "token_type" in json_response
