import os

import duckdb
import kuzu
from dotenv import find_dotenv, load_dotenv

from database.src import graph_edges, graph_nodes
from app.core.config import settings

load_dotenv(find_dotenv(".env"))
LOGIN = os.environ.get("HEURIST_LOGIN")
PASSWORD = os.environ.get("HEURIST_PASSWORD")


NODES: list[graph_nodes.Base] = [
    graph_nodes.Storyverse,
    graph_nodes.Story,
    graph_nodes.Text,
    graph_nodes.Witness,
    graph_nodes.Part,
    graph_nodes.Document,
    graph_nodes.Repository,
    graph_nodes.Place,
    graph_nodes.Genre,
    graph_nodes.Scripta,
    graph_nodes.Language,
]

EDGES = [
    graph_edges.IsPartOf,
    graph_edges.IsDerivedFrom,
    graph_edges.IsRealizedIn,
    graph_edges.IsEmbodiedIn,
    graph_edges.HasWritingStyle,
    graph_edges.HasGenre,
    graph_edges.IsMaterializedOn,
    graph_edges.IsLocated,
    graph_edges.HasLanguage,
]


def rebuild_graph(
    kuzu_db: kuzu.Connection = None,
    duck_conn: duckdb.DuckDBPyConnection = None,
):
    if not duck_conn:
        duck_conn = duckdb.connect(settings.DUCKDB_PATH)
    if not kuzu_db:
        db = kuzu.Database(settings.KUZU_PATH)
        kuzu_db = kuzu.Connection(db)

    # Delete all relationships, then delete all nodes
    for rel in EDGES + NODES:
        label = rel.__name__
        query = f"DROP TABLE IF EXISTS {label}"
        kuzu_db.execute(query=query)

    # Create the new nodes and relationships
    for node in NODES:
        node_table = node(conn=duck_conn)
        node_table.insert_nodes(kuzu_db)

    for edge in EDGES:
        rel_table = edge(conn=duck_conn)
        rel_table.insert_edges(kuzu_db)
