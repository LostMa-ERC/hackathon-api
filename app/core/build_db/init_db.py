import duckdb
import kuzu

from app.core.config import settings
from .build_graph import rebuild_graph
from .build_relational_db import refresh_data
from .build_witness_trees import build_witness_trees


def init_db():
    # Download new data from Heurist
    dconn = duckdb.connect(settings.DUCKDB_PATH)
    refresh_data(conn=dconn)

    # Convert the relational database into a Kùzu graph database
    kdb = kuzu.Database(settings.KUZU_PATH)
    with kuzu.Connection(database=kdb) as kconn:
        rebuild_graph(kuzu_db=kconn, duck_conn=dconn)

    # Build static witness trees
    build_witness_trees()
