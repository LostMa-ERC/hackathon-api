from duckdb import DuckDBPyConnection
from kuzu import Connection

from app.core.etl import models
from app.core.etl import rels


def test_storyverse_nodes(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = models.Storyverse(conn=duckdb_connection)
    model.insert_nodes(kuzu_connection=kuzu_connection)


def test_story_nodes(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = models.Story(conn=duckdb_connection)
    model.insert_nodes(kuzu_connection=kuzu_connection)


def test_text_nodes(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = models.Text(conn=duckdb_connection)
    model.insert_nodes(kuzu_connection=kuzu_connection)


def test_witness_nodes(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = models.Witness(conn=duckdb_connection)
    model.insert_nodes(kuzu_connection=kuzu_connection)


def test_part_nodes(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = models.Part(conn=duckdb_connection)
    model.insert_nodes(kuzu_connection=kuzu_connection)


def test_document_nodes(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = models.Document(conn=duckdb_connection)
    model.insert_nodes(kuzu_connection=kuzu_connection)


def test_Repository_nodes(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = models.Repository(conn=duckdb_connection)
    model.insert_nodes(kuzu_connection=kuzu_connection)


def test_place_nodes(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = models.Place(conn=duckdb_connection)
    model.insert_nodes(kuzu_connection=kuzu_connection)


def test_genre_nodes(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = models.Genre(conn=duckdb_connection)
    model.insert_nodes(kuzu_connection=kuzu_connection)


def test_scripta_nodes(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = models.Scripta(conn=duckdb_connection)
    model.insert_nodes(kuzu_connection=kuzu_connection)


def test_part_of_rel(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = rels.IsPartOf(conn=duckdb_connection)
    model.insert_edges(kuzu_connection=kuzu_connection)


def test_derived_from_rel(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = rels.IsDerivedFrom(conn=duckdb_connection)
    model.insert_edges(kuzu_connection=kuzu_connection)


def test_realized_in_rel(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = rels.IsRealizedIn(conn=duckdb_connection)
    model.insert_edges(kuzu_connection=kuzu_connection)


def test_embodied_in_rel(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = rels.IsEmbodiedIn(conn=duckdb_connection)
    model.insert_edges(kuzu_connection=kuzu_connection)


def test_has_writing_style_rel(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = rels.HasWritingStyle(conn=duckdb_connection)
    model.insert_edges(kuzu_connection=kuzu_connection)


def test_has_genre_rel(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = rels.HasGenre(conn=duckdb_connection)
    model.insert_edges(kuzu_connection=kuzu_connection)


def test_is_materialized_on_rel(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = rels.IsMaterializedOn(conn=duckdb_connection)
    model.insert_edges(kuzu_connection=kuzu_connection)


def test_is_located_rel(
    duckdb_connection: DuckDBPyConnection,
    kuzu_connection: Connection,
):
    model = rels.IsLocated(conn=duckdb_connection)
    model.insert_edges(kuzu_connection=kuzu_connection)
