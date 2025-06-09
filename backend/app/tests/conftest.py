from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.api.deps import SessionDep
from app.core.config import settings
from app.core.db import DB
from app.main import app


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[DB, None, None]:
    with SessionDep() as session:
        yield session


def pytest_configure():
    pytest.api_prefix = settings.API_V1_STR
