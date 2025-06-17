import os

import duckdb
from dotenv import find_dotenv, load_dotenv
from heurist.api.connection import HeuristAPIConnection
from heurist.workflows import extract_transform_load

load_dotenv(find_dotenv(".env"))
LOGIN = os.environ.get("HEURIST_LOGIN")
PASSWORD = os.environ.get("HEURIST_PASSWORD")


def refresh_data(conn: duckdb.DuckDBPyConnection):
    # Rewrite the tables in the DuckDB database with new data requested from Heurist
    with HeuristAPIConnection(
        db="jbcamps_gestes", login=LOGIN, password=PASSWORD
    ) as client:
        extract_transform_load(
            client=client,
            duckdb_connection=conn,
            record_group_names=["My record types", "Place, features"],
        )
