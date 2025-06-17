from typing import Annotated, AsyncGenerator

from fastapi import Depends

from app.core.config import settings
from app.core.db import GraphDB, RelationalDB


# Connect to a persistent Kuzu graph database
async def get_kuzu_session() -> AsyncGenerator[GraphDB, None]:
    with GraphDB(fp=settings.KUZU_PATH) as session:
        yield session


# Connect to the downloaded Heurist database
async def get_duckdb_session() -> AsyncGenerator[RelationalDB, None]:
    with RelationalDB(fp=settings.DUCKDB_PATH) as session:
        yield session


GraphDBSessionDep = Annotated[GraphDB, Depends(get_kuzu_session)]
RelationalDBSessionDep = Annotated[RelationalDB, Depends(get_duckdb_session)]
