# Finalized relations to expose through the API

from abc import ABC
from dataclasses import dataclass

from duckdb import DuckDBPyConnection
from kuzu import Connection


@dataclass
class Edge:
    _from_node: str
    _to_node: str

    def str(self) -> str:
        return f"FROM {self._from_node} TO {self._to_node}"


class Base(ABC):
    _attr: str | None = None

    def __init__(self, conn: DuckDBPyConnection):
        self.conn = conn
        assert len(self.edges) == len(self.selections)
        super().__init__()

    @property
    def edges(self) -> list[Edge]:
        pass

    @property
    def selections(self) -> str:
        pass

    def create_rel_stmt(self) -> str:
        name = self.__class__.__name__

        def edge_pair(edge: Edge) -> str:
            return f"FROM {edge._from_node} TO {edge._to_node}"

        pairs = ", ".join([edge_pair(edge=edge) for edge in self.edges])
        if self._attr:
            pairs += f", {self._attr} STRING"
        return f"CREATE REL TABLE {name}({pairs})"

    def insert_edges(self, kuzu_connection: Connection):
        name = self.__class__.__name__
        query = self.create_rel_stmt()
        kuzu_connection.execute(query)
        for edge, sql in zip(self.edges, self.selections):

            # Select the data from the relational database
            try:
                rel = self.conn.sql(sql)
                print(rel)
                df = rel.pl()
            except Exception as e:
                print(query)
                raise e

            # Insert the data into the graph database
            query = (
                f"COPY {name} FROM df (from='{edge._from_node}', to='{edge._to_node}')"
            )
            try:
                kuzu_connection.execute(query)
            except Exception as e:
                print(query)
                raise e

            # Confirm that all the edges were added
            query = f"""MATCH (a:{edge._from_node})-[r:{name}]->(b:{edge._to_node})
            RETURN a.id, b.id"""
            rels = kuzu_connection.execute(query).get_as_pl()
            assert df.shape[0] == rels.shape[0]


class IsPartOf(Base):
    edges = [Edge("Storyverse", "Storyverse"), Edge("Story", "Storyverse")]

    selections = [
        """
SELECT
    "H-ID" AS "from",
    unnest("member_of_cycle H-ID") AS "to"
FROM Storyverse
WHERE "member_of_cycle H-ID" != []
""",
        """
SELECT
    "H-ID" AS "from",
    unnest("is_part_of_storyverse H-ID") AS "to"
FROM Story
WHERE "is_part_of_storyverse H-ID" != []
""",
    ]


class IsDerivedFrom(Base):
    edges = [Edge("Story", "Story"), Edge("Text", "Text")]

    selections = [
        """
SELECT
    "H-ID" AS "from",
    unnest("is_modeled_on H-ID") AS "to"
FROM Story
WHERE "is_modeled_on H-ID" != []
""",
        """
SELECT
    "H-ID" AS "from",
    unnest("is_derived_from H-ID") AS "to"
FROM TextTable
WHERE "is_derived_from H-ID" != []
""",
    ]


class IsRealizedIn(Base):
    edges = [Edge("Story", "Text")]
    _attr = "lrm"

    selections = [
        """
SELECT
    unnest("is_expression_of H-ID") AS "from",
    "H-ID" AS "to",
    'R3' AS lrm
FROM TextTable
WHERE "is_expression_of H-ID" != []
"""
    ]


class IsEmbodiedIn(Base):
    edges = [Edge("Text", "Witness")]
    _attr = "lrm"

    selections = [
        """
SELECT
    "is_manifestation_of H-ID" AS "from",
    "H-ID" AS "to",
    'R4' AS lrm
FROM Witness
WHERE "from" IS NOT NULL
    """,
    ]


class HasWritingStyle(Base):
    edges = [Edge("Text", "Scripta"), Edge("Witness", "Scripta")]

    selections = [
        """
SELECT
    "H-ID" AS "from",
    "regional_writing_style H-ID" AS "to"
FROM TextTable
WHERE "to" IS NOT NULL
""",
        """
SELECT
    "H-ID" AS "from",
    "regional_writing_style H-ID" AS "to"
FROM Witness
WHERE "to" IS NOT NULL
""",
    ]


class HasGenre(Base):
    edges = [Edge("Text", "Genre")]

    selections = [
        """
SELECT
    "H-ID" AS "from",
    "specific_genre H-ID" AS "to"
FROM TextTable
WHERE "to" IS NOT NULL
"""
    ]


class IsMaterializedOn(Base):
    edges = [Edge("Witness", "Part"), Edge("Part", "Document")]
    _attr = "lrm"

    selections = [
        """
SELECT
    "H-ID" AS "from",
    unnest("observed_on_pages H-ID") AS "to",
    'R7' AS lrm
FROM Witness
WHERE "observed_on_pages H-ID" != []
""",
        """
SELECT
    "H-ID" AS "from",
    "is_inscribed_on H-ID" AS "to",
    'R7' AS lrm
FROM Part
WHERE "to" IS NOT NULL
""",
    ]


class IsLocated(Base):
    edges = [Edge("Document", "Repository"), Edge("Repository", "Place")]

    selections = [
        """
SELECT
    "H-ID" AS "from",
    "location H-ID" AS "to"
FROM DocumentTable
WHERE "to" IS NOT NULL
""",
        """
SELECT
    "H-ID" AS "from",
    "city H-ID" AS "to"
FROM Repository
WHERE "to" IS NOT NULL
""",
    ]
