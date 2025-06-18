from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

import database.config


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_URL: str = "TBD"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    DUCKDB_PATH: Path = database.config.RELATIONAL_DB_PATH
    KUZU_PATH: Path = database.config.GRAPH_DB_PATH
    STATIC_DIR: Path = Path(__file__).parent.parent.joinpath("static")

    PROJECT_NAME: str = "Hackathon API"


settings = Settings()
