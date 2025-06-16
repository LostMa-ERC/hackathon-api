from fastapi.testclient import TestClient

from app.core.config import settings

COLLECTION_PREFIX = f"{settings.API_V1_STR}/collection"


def test_storyverse_collection(client: TestClient):
    url = COLLECTION_PREFIX + "/storyverse/"
    response1 = client.get(url=url)
    general1 = response1.json()

    url = COLLECTION_PREFIX + "/storyverse/?id=general"
    response2 = client.get(url=url)
    general2 = response2.json()

    assert len(general1["member"]) > 0
    assert general1 == general2


def test_story_collection(client: TestClient):
    url = COLLECTION_PREFIX + "/story/?id=170"
    response = client.get(url=url)
    data = response.json()
    assert len(data["member"]) == 1
    assert data["member"][0]["@id"] == 170


def test_text_collection(client: TestClient):
    url = COLLECTION_PREFIX + "/text/"
    response1 = client.get(url=url)
    general1 = response1.json()

    url = COLLECTION_PREFIX + "/text/?id=general"
    response2 = client.get(url=url)
    general2 = response2.json()

    assert len(general1["member"]) > 0
    assert general1 == general2
