import os

import duckdb
from dotenv import find_dotenv, load_dotenv
from heurist.api.connection import HeuristAPIConnection
from heurist.workflows import extract_transform_load

from app.core.db import DB
from app.core.etl import models, rels

load_dotenv(find_dotenv(".env"))
LOGIN = os.environ.get("HEURIST_LOGIN")
PASSWORD = os.environ.get("HEURIST_PASSWORD")


NODES: list[models.Base] = [
    models.Storyverse,
    models.Story,
    models.Text,
    models.Witness,
    models.Part,
    models.Document,
    models.Repository,
    models.Place,
    models.Genre,
    models.Scripta,
]

EDGES = [
    rels.IsPartOf,
    rels.IsDerivedFrom,
    rels.IsRealizedIn,
    rels.IsEmbodiedIn,
    rels.HasWritingStyle,
    rels.HasGenre,
    rels.IsMaterializedOn,
    rels.IsLocated,
]


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


def rebuild_graph(kuzu_db: DB, duck_conn: duckdb.DuckDBPyConnection):

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
