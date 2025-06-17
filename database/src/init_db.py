import duckdb
import kuzu

from database.config import GRAPH_DB_PATH, RELATIONAL_DB_PATH
from database.src.build_graph import rebuild_graph
from database.src.build_relational_db import refresh_data


def init_db():
    dconn = duckdb.connect(RELATIONAL_DB_PATH)
    refresh_data(conn=dconn)
    kdb = kuzu.Database(GRAPH_DB_PATH)
    kconn = kuzu.Connection(database=kdb)
    rebuild_graph(kuzu_db=kconn, duck_conn=dconn)
