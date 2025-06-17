from pathlib import Path

dir = Path(__file__).parent

RELATIONAL_DB_PATH = dir.joinpath("heurist.duckdb")
GRAPH_DB_PATH = dir.joinpath("kuzu_db")
