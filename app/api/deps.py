from typing import Annotated, AsyncGenerator

from fastapi import Depends

from app.core.config import settings
from app.core.db import DB


# Connect to a persistent Kuzu graph database
async def get_session() -> AsyncGenerator[DB]:
    with DB(fp=settings.KUZU_PATH) as session:
        yield session


SessionDep = Annotated[DB, Depends(get_session)]
