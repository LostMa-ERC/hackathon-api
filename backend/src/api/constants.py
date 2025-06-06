from pathlib import Path

DATADIR = Path(__file__).parent.parent.parent.joinpath("data")
DATADIR.mkdir(exist_ok=True)

DATABASE_FP = DATADIR.joinpath("heurist.duckdb")
