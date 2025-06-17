# Finalized fields to publish through the API

from abc import ABC
from dataclasses import dataclass
from typing import Optional

from duckdb import DuckDBPyConnection
from kuzu import Connection


@dataclass
class Field:
    column: str
    type: str
    alias: Optional[str] = None

    def __post_init__(self):
        if self.alias is None:
            self.alias = self.column


HID = Field(column="H-ID", alias="id", type="INT64")


@dataclass
class Name:
    table_name: str
    node_label: Optional[str] = None

    def __post_init__(self):
        if self.node_label is None:
            self.node_label = self.table_name


class Base(ABC):

    def __init__(self, conn: DuckDBPyConnection):
        self.conn = conn
        super().__init__()

    @property
    def fields(self) -> list[Field]:
        pass

    @property
    def _from(self) -> str:
        pass

    def make_select_stmt(self) -> str:
        def alias_stmt(field: Field) -> str:
            if (
                field.column.lower().startswith("case when")
                or field.type == "DATE"
                or len(field.column.split(".")) > 1
            ):
                return f"{field.column} as {field.alias}"
            else:
                return f'"{field.column}" AS "{field.alias}"'

        aliases = ", ".join([alias_stmt(field) for field in self.fields])
        return f"SELECT {aliases}"

    def pl(self):
        select = self.make_select_stmt()
        query = f"{select} {self._from}"
        try:
            return self.conn.sql(query=query).pl()
        except Exception as e:
            print(query)
            raise e

    def create_node_stmt(self) -> str:
        name = self.__class__.__name__
        start = f"CREATE NODE TABLE {name}("
        fields = ", ".join([f"{f.alias} {f.type}" for f in self.fields])
        end = ", PRIMARY KEY(id))"
        return f"{start}{fields}{end}"

    def insert_nodes(self, kuzu_connection: Connection):
        query = self.create_node_stmt()
        kuzu_connection.execute(query)
        df = self.pl()
        name = self.__class__.__name__
        kuzu_connection.execute(f"COPY {name} FROM df")
        nodes = kuzu_connection.execute(f"MATCH (n:{name}) RETURN n.*").get_as_pl()
        # Confirm that all the rows in the SQL relation were
        # inserted into the Kuzu nodes table
        assert df.shape == nodes.shape


class Storyverse(Base):
    fields = [
        HID,
        Field(column="preferred_name", alias="name", type="STRING"),
        Field(column="alternative_names", type="STRING[]"),
        Field(column="described_at_URL", alias="urls", type="STRING[]"),
    ]

    _from = """FROM Storyverse"""

    def __init__(self, conn: DuckDBPyConnection):
        self.conn = conn


class Story(Base):
    fields = [
        HID,
        Field(column="preferred_name", alias="name", type="STRING"),
        Field(column="alternative_names", type="STRING[]"),
        Field(column="matter", type="STRING"),
        Field(
            column="case when peripheral like 'Yes' then true else false end",
            alias="peripheral",
            type="BOOLEAN",
        ),
        Field(column="described_at_URL", alias="urls", type="STRING[]"),
    ]

    _from = """FROM Story"""


class Text(Base):
    fields = [
        HID,
        Field(column="preferred_name", alias="name", type="STRING"),
        Field(column="alternative_names", type="STRING[]"),
        Field(column="literary_form", alias="form", type="STRING"),
        Field(
            column="case when is_hypothetical like 'Yes' then true else false end",
            alias="is_hypothetical",
            type="BOOLEAN",
        ),
        Field(
            column="case when peripheral like 'Yes' then true else false end",
            alias="peripheral",
            type="BOOLEAN",
        ),
        Field(column="length", type="DOUBLE"),
        Field(column="verse_type", type="STRING[]"),
        Field(column="rhyme_type", type="STRING[]"),
        Field(column="Stanza_type", alias="stanza_type", type="STRING"),
        Field(column="nature_of_derivations", type="STRING"),
        Field(column="tradition_status", alias="status", type="STRING"),
        Field(column="status_notes", type="STRING"),
        Field(
            column="date_of_creation.estMinDate",
            alias="creation_date_min",
            type="DATE",
        ),
        Field(
            column="date_of_creation.estMaxDate",
            alias="creation_date_max",
            type="DATE",
        ),
        Field(
            column="date_of_creation.value",
            alias="creation_date_year",
            type="DATE",
        ),
        Field(
            column="date_of_creation_certainty",
            alias="creation_date_certainty",
            type="STRING",
        ),
        Field(column="date_freetext", alias="creation_date_text", type="STRING"),
        Field(column="described_at_URL", alias="urls", type="STRING[]"),
    ]

    _from = """FROM TextTable"""


class Witness(Base):
    fields = [
        HID,
        Field(
            column="case when is_unobserved like 'Yes' then true else false end",
            alias="is_unobserved",
            type="BOOLEAN",
        ),
        Field(column="preferred_siglum", alias="siglum", type="STRING"),
        Field(column="alternative_sigla", type="STRING[]"),
        Field(column="status_witness", alias="status", type="STRING"),
        Field(
            column="case when is_excerpt like 'Yes' then true else false end",
            alias="is_excerpt",
            type="BOOLEAN",
        ),
        Field(
            column="date_of_creation.estMinDate",
            alias="creation_date_min",
            type="DATE",
        ),
        Field(
            column="date_of_creation.estMaxDate",
            alias="creation_date_max",
            type="DATE",
        ),
        Field(
            column="date_of_creation.value",
            alias="creation_date_year",
            type="DATE",
        ),
        Field(
            column="date_of_creation_certainty",
            alias="creation_date_certainty",
            type="STRING",
        ),
        Field(column="date_freetext", alias="creation_date_text", type="STRING"),
        Field(column="number_of_hands", type="DOUBLE"),
        Field(column="described_at_URL", alias="urls", type="STRING[]"),
    ]

    _from = "FROM Witness"


class Part(Base):
    fields = [
        Field(column='pt."H-ID"', alias="id", type="INT64"),
        Field(column="pt.div_order", alias="div_order", type="INT8"),
        Field(column="pt.number_of_verses", alias="number_of_verses", type="INT64"),
        Field(column="pt.part_of_text", alias="part_of_text", type="STRING"),
        Field(column="pt.volume_number", alias="volume_number", type="STRING"),
        Field(column="pt.number_of_lines", alias="number_of_lines", type="INT64"),
        Field(column="pt.verses_per_line", alias="verses_per_line", type="STRING"),
        Field(
            column="""case when pt.lines_are_incomplete like 'Yes'\
then true else false end""",
            alias="lines_are_incomplete",
            type="BOOLEAN",
        ),
        Field(column="pt.page_ranges", alias="page_ranges", type="STRING[]"),
        Field(column="pd.material", alias="material", type="STRING"),
        Field(column="pd.form", alias="form", type="STRING"),
        Field(column="pd.folio_size_height", alias="folio_size_height", type="STRING"),
        Field(column="pd.folio_size_width", alias="folio_size_width", type="STRING"),
        Field(
            column="pd.estimated_folio_size_height",
            alias="estimated_folio_size_height",
            type="STRING",
        ),
        Field(
            column="pd.estimated_folio_size_width",
            alias="estimated_folio_size_width",
            type="STRING",
        ),
        Field(
            column="pd.writing_surface_area_height",
            alias="writing_surface_area_height",
            type="STRING",
        ),
        Field(column="pd.number_of_columns", alias="number_of_columns", type="STRING"),
        Field(column="pd.above_top_line", alias="above_top_line", type="STRING"),
        Field(column="pd.script_type", alias="script_type", type="STRING"),
        Field(column="pd.subscript_type", alias="subscript_type", type="STRING"),
        Field(column="pd.has_decorations", alias="has_decorations", type="STRING[]"),
        Field(
            column="pd.amount_of_illustrations",
            alias="amount_of_illustrations",
            type="STRING",
        ),
    ]

    _from = """
FROM Part pt
LEFT JOIN PhysDesc pd
    ON pt."is_inscribed_on H-ID" = pd."H-ID"
"""


class Document(Base):
    fields = [
        HID,
        Field(column="current_shelfmark", alias="shelfmark", type="STRING"),
        Field(column="old_shelfmark", alias="old_shelfmarks", type="STRING[]"),
        Field(
            column="contents_of_record_without_shelfmark",
            alias="contents_of_record_without_shelfmark",
            type="STRING",
        ),
        Field(column="collection", alias="collection", type="STRING"),
        Field(
            column="case when is_hypothetical like 'Yes' then true else false end",
            alias="is_hypothetical",
            type="BOOLEAN",
        ),
        Field(
            column="collection_of_fragments",
            alias="collection_of_fragments",
            type="STRING",
        ),
        Field(column="described_at_URL", alias="urls", type="STRING[]"),
        Field(column="online_catalogue_URL", alias="catalogue_url", type="STRING"),
        Field(column="ARK", alias="ark", type="STRING"),
    ]

    _from = """FROM DocumentTable"""


class Repository(Base):
    fields = [
        HID,
        Field(column="preferred_name", alias="name", type="STRING"),
        Field(column="alternative_names", alias="alternative_names", type="STRING[]"),
        Field(column="VIAF", alias="viaf", type="STRING"),
        Field(column="ISNI", alias="isni", type="STRING"),
        Field(column="biblissima_identifier", alias="biblissima", type="STRING"),
        Field(column="website", alias="website", type="STRING"),
    ]

    _from = """FROM Repository"""


class Place(Base):
    fields = [
        HID,
        Field(column="place_name", alias="name", type="STRING"),
        Field(column="administrative_region", alias="region", type="STRING"),
        Field(column="country", type="STRING"),
        Field(column="place_type", type="STRING"),
        Field(column="location_mappable", type="STRING"),
        Field(column="location_certainty", type="STRING"),
        Field(column="geonames_id", type="STRING"),
    ]

    _from = "FROM Place"


class Genre(Base):
    fields = [
        HID,
        Field(column="preferred_name", alias="name", type="STRING"),
        Field(column="alternative_names", type="STRING[]"),
        Field(column="description", type="STRING"),
        Field(column="archetype", type="STRING"),
        Field(column="described_at_URL", alias="urls", type="STRING[]"),
    ]

    _from = "FROM Genre"


class Scripta(Base):
    fields = [
        HID,
        Field(column="preferred_name", alias="name", type="STRING"),
        Field(column="description", type="STRING"),
        Field(column="described_at_URL", alias="urls", type="STRING[]"),
    ]

    _from = "FROM Scripta"


class Language(Base):
    fields = [
        Field(column="trm_ID", alias="id", type="INT64"),
        Field(column="trm_Label", alias="name", type="STRING"),
        Field(column="trm_Description", alias="description", type="STRING"),
        Field(column="trm_Code", alias="code", type="STRING"),
        Field(column="trm_SemanticReferenceURL", alias="url", type="STRING"),
    ]

    _from = "FROM trm WHERE trm_ParentTermID = 9469"
