import pytest
from fastapi.testclient import TestClient

ENDPOINT = f"{pytest.api_prefix}/"


def test_index(client: TestClient):
    required_keys = sorted(
        [
            "@context",
            "@type",
            "document",
            "navigation",
            "@id",
            "collection",
            "dtsVersion",
        ]
    )
    result = client.get(ENDPOINT)
    actual_keys = sorted(list(result.json().keys()))
    assert required_keys == actual_keys
