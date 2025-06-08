from app.core.db import DB
from app.api.deps import SessionDep


def test_db():
    with SessionDep() as session:
        assert isinstance(session, DB)
