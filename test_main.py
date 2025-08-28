from fastapi import status

from base_test import BaseTest


class TestMain(BaseTest):
    def test_read_main(self, initialize_cache):
        response = self.client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"response": "my test"}
