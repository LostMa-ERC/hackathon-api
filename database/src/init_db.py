import duckdb
import kuzu

from database.config import GRAPH_DB_PATH, RELATIONAL_DB_PATH
from database.src.build_graph import rebuild_graph
from database.src.build_relational_db import refresh_data
from database.src.build_witness_trees import build_witness_trees


def init_db():
    # Download new data from Heurist
    dconn = duckdb.connect(RELATIONAL_DB_PATH)
    refresh_data(conn=dconn)

    # Convert the relational database into a Kùzu graph database
    kdb = kuzu.Database(GRAPH_DB_PATH)
    with kuzu.Connection(database=kdb) as kconn:
        rebuild_graph(kuzu_db=kconn, duck_conn=dconn)

    # Build static witness trees
    build_witness_trees()
