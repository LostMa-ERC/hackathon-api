from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

DATADIR = Path(__file__).parent.parent.parent.joinpath("data")
DATADIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level about ./backend)
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_URL: str = "TBD"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    DUCKDB_PATH: Path = DATADIR.joinpath("heurist.duckdb")
    KUZU_PATH: Path = DATADIR.joinpath("kuzu_db")

    PROJECT_NAME: str


settings = Settings()
