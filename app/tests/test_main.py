from fastapi import status

from app.core.base_test import BaseTest


class TestMain(BaseTest):
    def test_read_main(self, initialize_cache):
        response = self.client.get(f"{self.url_version}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"response": "my test"}
