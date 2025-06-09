from collections import namedtuple

from app.core.db import DB

Join = namedtuple("Join", field_names=["table_name", "t0_col", "on_col"])


class SQLBuilder:
    where_condition = None
    limit_condition = None

    def __init__(
        self,
        table_name: str,
        primary_key: str = "H-ID",
        offset: int = 0,
        limit: int = 0,
        id: int = None,
    ):
        self.table_name = table_name
        self.order_condition = f'ORDER BY "{primary_key}"'
        if id:
            self.where_condition = f'WHERE "H-ID" = {id}'
        if limit != 0:
            self.limit_condition = f"LIMIT {limit}"
        self.offset_condition = f"OFFSET {offset}"

    @property
    def conditions(self) -> str:
        conditions = [
            self.where_condition,
            self.order_condition,
            self.limit_condition,
            self.offset_condition,
        ]
        return " ".join([cond for cond in conditions if cond])

    def execute_query(self, session: DB, query: str, params: list = []) -> list[dict]:
        try:
            return session.get_dict_array(query=query, paramaters=params)
        except Exception as e:
            print(query)
            raise e

    def select_table(self) -> list[dict]:
        return f"SELECT * FROM {self.table_name} {self.conditions}"

    def join_tables(self, joins: list[Join]) -> list[dict]:
        # Get the selection aliases
        selections = [r'SELECT COLUMNS(t0.*) AS "t0_\0"']
        for n, _ in enumerate(joins):
            n += 1
            s = f'COLUMNS(t{n}.*) AS "t{n}_' + r'\0"'
            selections.append(s)
        selection = ", ".join(selections)

        # Get the from tables
        from_stmts = [f"FROM {self.table_name} t0"]
        for n, join in enumerate(joins):
            n += 1
            s = f"""\
LEFT JOIN {join.table_name} t{n}
ON t0."{join.t0_col}" = t{n}."{join.on_col}"\
"""
            from_stmts.append(s)
        from_stmt = " ".join(from_stmts)

        # Put it all together!
        self.order_condition = 'ORDER BY t0."H-ID"'
        return f"{selection} {from_stmt} {self.conditions}"
