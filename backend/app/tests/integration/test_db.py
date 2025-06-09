from datetime import datetime

from app.core.db import DB


def test_refresh_db(db: DB) -> None:
    start = datetime.now()
    db.refresh_data()
    end = datetime.now()
    assert start < end
