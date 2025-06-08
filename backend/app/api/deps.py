from typing import Annotated, Generator

from fastapi import Depends

from app.core.db import DB


# Connect to a persistent DuckDB database
def get_session() -> Generator[DB]:
    with DB() as session:
        yield session


SessionDep = Annotated[DB, Depends(get_session)]
