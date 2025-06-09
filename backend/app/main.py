from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.core.db import DB


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Download new data upon start up the server
    if not settings.DB_PATH.is_file() or settings.ENVIRONMENT == "production":
        with DB(settings.DB_PATH) as db:
            db.refresh_data()
    yield


# Create an instance of FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Prepare app for communicating with frontend
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
