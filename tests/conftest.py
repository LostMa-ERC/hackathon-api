from collections.abc import Generator

import duckdb
import pytest
from fastapi.testclient import TestClient

from app.api.deps import SessionDep
from app.core.config import settings
from app.core.db import DB
from app.main import app
from db.refresh import init_db

if not settings.DUCKDB_PATH.is_file():
    init_db()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[DB, None, None]:
    with SessionDep() as session:
        yield session


@pytest.fixture(scope="module")
def duckdb_connection() -> Generator[duckdb.DuckDBPyConnection, None, None]:
    with duckdb.connect(settings.DUCKDB_PATH) as conn:
        yield conn


@pytest.fixture(scope="module")
def writeable_db() -> Generator[DB, None, None]:
    with SessionDep(read_only=False) as session:
        yield session


def pytest_configure():
    pytest.api_prefix = settings.API_V1_STR
