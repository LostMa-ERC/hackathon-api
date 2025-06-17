from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.api.deps import GraphDBSessionDep, RelationalDBSessionDep
from app.core.config import settings
from app.core.db import GraphDB, RelationalDB
from app.main import app
from database.src.init_db import init_db

if not settings.DUCKDB_PATH.is_file():
    init_db()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def graph_db() -> Generator[GraphDB, None, None]:
    with GraphDBSessionDep() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def rel_db() -> Generator[RelationalDB, None, None]:
    with RelationalDBSessionDep() as session:
        yield session


@pytest.fixture(scope="module")
def writeable_rel_db() -> Generator[RelationalDB, None, None]:
    with RelationalDBSessionDep(read_only=False) as session:
        yield session


@pytest.fixture(scope="module")
def writeable_graph_db() -> Generator[GraphDB, None, None]:
    with GraphDBSessionDep(read_only=False) as session:
        yield session


def pytest_configure():
    pytest.api_prefix = settings.API_V1_STR
