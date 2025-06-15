import kuzu

from app.core.config import settings


class DB:
    def __init__(
        self, fp: str | None = settings.KUZU_PATH, read_only: bool = True
    ) -> None:
        self.fp = fp
        self.read_only = read_only

    def __enter__(self):
        # If the database has never been created, create an empty one in write-read mode
        if not self.fp.is_dir():
            _ = kuzu.Database(database_path=self.fp, read_only=False)

        # Assuming the database is created, instantiate it in read-only
        # (unless otherwise specified in the DB init)
        try:
            db = kuzu.Database(database_path=self.fp, read_only=self.read_only)
        except RuntimeError as e:
            raise e

        # Make a connection to the database
        self.conn = kuzu.Connection(db)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def execute(self, query: str, parameters: dict = {}) -> kuzu.QueryResult:
        return self.conn.execute(query=query, parameters=parameters)

    def get_rows(self, query: str, parameters: dict = {}) -> list:
        result = self.execute(query=query, parameters=parameters)
        rows = []
        while result.has_next():
            values = result.get_next()
            rows.append(values)
        return rows
