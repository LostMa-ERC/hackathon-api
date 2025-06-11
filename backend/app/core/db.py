import duckdb

from app.core.config import settings


class DB:
    def __init__(self, fp: str | None = settings.DUCKDB_PATH) -> None:
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
