from datetime import datetime

import pytest

from db import refresh


@pytest.mark.dependency()
def test_refresh_db(duckdb_connection) -> None:
    start = datetime.now()
    refresh.refresh_data(conn=duckdb_connection)
    end = datetime.now()
    assert start < end


@pytest.mark.dependency(depends=["test_refresh_db"])
def test_rebuild_graph(writeable_db, duckdb_connection) -> None:
    start = datetime.now()
    refresh.rebuild_graph(kuzu_db=writeable_db, duck_conn=duckdb_connection)
    end = datetime.now()
    assert start < end
