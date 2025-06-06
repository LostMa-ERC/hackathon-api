import unittest
from datetime import datetime

from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


class Test(unittest.TestCase):

    def test_refresh_database(self):
        # Get a response from the TestClient
        response = client.put("/")

        # Assert that the response is good
        self.assertEqual(response.status_code, 200)

        message = response.json()
        start = datetime.fromisoformat(message["updateDuration"]["start"])
        end = datetime.fromisoformat(message["updateDuration"]["end"])

        self.assertGreater(end, start)


if __name__ == "__main__":
    unittest.main()
