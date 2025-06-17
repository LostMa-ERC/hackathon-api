from datetime import datetime

import pytest

from database.src.build_graph import rebuild_graph
from database.src.build_relational_db import refresh_data


@pytest.mark.dependency()
def test_refresh_db(writeable_rel_db) -> None:
    start = datetime.now()
    refresh_data(conn=writeable_rel_db)
    end = datetime.now()
    assert start < end


@pytest.mark.dependency(depends=["test_refresh_db"])
def test_rebuild_graph(writeable_graph_db, writeable_rel_db) -> None:
    start = datetime.now()
    rebuild_graph(kuzu_db=writeable_graph_db, duck_conn=writeable_rel_db)
    end = datetime.now()
    assert start < end
