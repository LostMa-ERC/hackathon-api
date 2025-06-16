from fastapi.testclient import TestClient

from app.core.config import settings

COLLECTION_PREFIX = f"{settings.API_V1_STR}/collection/"


def test_full_collection(client: TestClient):
    url = COLLECTION_PREFIX + "?id=Storyverse"
    data = client.get(url=url).json()
    assert len(data["member"]) > 0


def test_target_node(client: TestClient):
    # Run test on Text node of ID 49515
    url = COLLECTION_PREFIX + "?id=49515"
    data = client.get(url=url).json()
    assert len(data["member"]) == 1
    assert data["member"][0]["@id"] == 49515
    # This Text is connected to more than 1 child Witness
    assert data["member"][0]["totalChildren"] > 0
