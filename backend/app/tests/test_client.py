import unittest

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)


class Test(unittest.TestCase):

    def test_refresh_database(self):
        # Get a response from the TestClient
        response = client.put(f"{settings.API_V1_STR}/db")

        # Assert that the response is good
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
