from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api.main import api_router
from app.core.config import settings
from app.core.build_db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # If the data sources are missing or if in deploying for production,
    # renew the data upon the server's start up
    if (
        not settings.DUCKDB_PATH.is_file()
        or not settings.KUZU_PATH
        or settings.ENVIRONMENT == "production"
    ):
        print("Initializing database with new data from Heurist.")
        init_db()
        print(f"Saved Heurist data in DuckDB database file at: {settings.DUCKDB_PATH}")
        print(f"Modelled relational data as graph database at: {settings.KUZU_PATH}")
        print(
            f"Wrote witness tree JSON files at: {settings.STATIC_DIR.joinpath("resource")}"
        )
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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = Path(__file__).parent.joinpath("static").joinpath("favicon.ico")
    return FileResponse(favicon_path)
