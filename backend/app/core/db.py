import os

import duckdb
from dotenv import find_dotenv, load_dotenv
from heurist.api.connection import HeuristAPIConnection
from heurist.workflows import extract_transform_load

from app.core.constants import DATABASE_FP

load_dotenv(find_dotenv(".env"))
LOGIN = os.environ.get("HEURIST_LOGIN")
PASSWORD = os.environ.get("HEURIST_PASSWORD")


class DB:
    def __init__(self, fp: str | None = DATABASE_FP) -> None:
        self.fp = fp

    def __enter__(self):
        self.conn = duckdb.connect(self.fp)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def execute(self, query: str, paramaters: list | dict = None) -> None:
        try:
            self.conn.execute(query=query, parameters=paramaters)
        except Exception as e:
            print(query)
            raise e

    def get_dict_array(self, query: str, paramaters: list | dict = None) -> list[dict]:
        try:
            rel = self.conn.sql(query=query, params=paramaters)
        except Exception as e:
            print(query)
            raise e
        cols = rel.columns
        return [{k: v for k, v in zip(cols, row)} for row in rel.fetchall()]

    def refresh_data(self):
        with HeuristAPIConnection(
            db="jbcamps_gestes", login=LOGIN, password=PASSWORD
        ) as client:
            extract_transform_load(
                client=client,
                duckdb_connection=self.conn,
                record_group_names=["My record types", "Place, features"],
            )
