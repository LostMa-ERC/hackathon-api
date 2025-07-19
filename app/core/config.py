from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

# Directory for the databases and static files
DATA_DIR = Path(__file__).parent.parent.parent.joinpath("data")
DATA_DIR.mkdir(exist_ok=True)

# Paths to the embedded databases
RELATIONAL_DB_PATH = DATA_DIR.joinpath("heurist.duckdb")
GRAPH_DB_PATH = DATA_DIR.joinpath("kuzu_db")

# Directory for the static files
STATIC_DIR = DATA_DIR.joinpath("static")
STATIC_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_URL: str = "TBD"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    DUCKDB_PATH: Path = RELATIONAL_DB_PATH
    KUZU_PATH: Path = GRAPH_DB_PATH
    STATIC_DIR: Path = STATIC_DIR

    PROJECT_NAME: str = "Hackathon API"


settings = Settings()
