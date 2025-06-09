import pytest
from fastapi import Response
from fastapi.testclient import TestClient

ENDPOINT = f"{pytest.api_prefix}/entities"


def assert_item_count(
    response: Response,
    equal_to: int = None,
    greater_than: int = None,
):
    assert response.status_code == 200
    data = response.json()
    count = data["count"]
    if equal_to:
        assert count == equal_to
    elif greater_than:
        assert count > greater_than
    if count > 0:
        first_item = data["items"][0]
        assert first_item != {}


def test_language(client: TestClient) -> None:
    url = f"{ENDPOINT}/language"
    response = client.get(url=url)
    # assert_item_count(response=response, greater_than=10)
    data = response.json()
    print(data)
    assert data["items"][0]["id"] is not None


def test_storyverse(client: TestClient) -> None:
    url = f"{ENDPOINT}/storyverse"
    response = client.get(url=url)
    assert_item_count(response=response, greater_than=10)


def test_story(client: TestClient) -> None:
    # Assert that the first results page has 100 items
    url = f"{ENDPOINT}/story"
    response = client.get(url=url)
    assert_item_count(response=response, equal_to=100)
    first_page = response.json()["items"]

    # Assert that the second results page has 100 items
    url = f"{ENDPOINT}/story?offset=100"
    response = client.get(url=url)
    assert_item_count(response=response, equal_to=100)
    print(response.json())
    second_page = response.json()["items"]

    # Assert that the first and second pages do not have the same items
    for item in first_page:
        assert item not in second_page

    # Assert that a results page beyond the table's scope has 0 items
    url = f"{ENDPOINT}/story?offset=500"
    response = client.get(url=url)
    assert_item_count(response=response, equal_to=0)

    # Assert that a targeted story is found
    url = f"{ENDPOINT}/story?id=61"
    response = client.get(url=url)
    assert_item_count(response=response, equal_to=1)


def test_text(client: TestClient) -> None:
    url = f"{ENDPOINT}/text?limit=10"
    response = client.get(url=url)
    assert_item_count(response=response, equal_to=10)
