from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class Place(BaseModel):
    id: int
    name: str
    region: Optional[str] = Field(default=[])
    country: Optional[str] = Field(default=None)
    place_type: Optional[str] = Field(default=None)
    location_mappable: Optional[str] = Field(default=None)
    location_certainty: Optional[str] = Field(default=None)
    geonames_id: Optional[int] = Field(default=None)


class Repository(BaseModel):
    # Properties of the Repository node
    id: int
    name: str
    alternative_names: List[Optional[str]] = Field(default=[])
    viaf: Optional[str] = Field(default=[])
    isni: Optional[str] = Field(default=[])
    biblissima_identifier: Optional[str] = Field(default=[])
    website: Optional[str] = Field(default=[])

    # Nested nodes
    settlement: Optional[Place] = Field(default=None)


class Part(BaseModel):
    # Properties of the Part node
    id: int
    div_order: int
    number_of_verses: Optional[int] = Field(default=None)
    part_of_text: Optional[str] = Field(default=None)
    volume_number: Optional[str] = Field(default=None)
    number_of_lines: Optional[int] = Field(default=None)
    verses_per_line: Optional[str] = Field(default=None)
    lines_are_incomplete: Optional[str] = Field(default=None)
    page_ranges: List[Optional[str]] = Field(default=[])
    material: Optional[str] = Field(default=None)
    form: Optional[str] = Field(default=None)
    folio_size_height: Optional[str] = Field(default=None)
    folio_size_width: Optional[str] = Field(default=None)
    estimated_folio_size_height: Optional[str] = Field(default=None)
    estimated_folio_size_width: Optional[str] = Field(default=None)
    writing_surface_area_height: Optional[str] = Field(default=None)
    writing_surface_area_width: Optional[str] = Field(default=None)
    number_of_columns: Optional[str] = Field(default=None)
    above_top_line: Optional[str] = Field(default=None)
    script_type: Optional[str] = Field(default=None)
    subscript_type: Optional[str] = Field(default=None)
    amount_of_illustrations: Optional[str] = Field(default=None)
    has_initials: bool
    has_rubrication: bool
    has_incomplete_decoration: bool
    has_no_decoration: bool
    has_pictorial_designs: bool
    decoration_is_unknown: bool


class Document(BaseModel):
    # Properties of the Document node
    id: int
    shelfmark: Optional[str] = Field(default=None)
    old_shelfmarks: List[Optional[str]] = Field(default=[])
    collection: Optional[str] = Field(default=None)
    is_hypothetical: bool
    collection_of_fragments: Optional[str] = Field(default=None)
    urls: List[Optional[str]] = Field(default=[])
    ark: Optional[str] = Field(default=None)

    # Nested nodes
    witness_parts: List[Optional[Part]] = Field(default=[])
    repository: Optional[Repository] = Field(default=None)


class Scripta(BaseModel):
    id: int
    name: str
    description: Optional[str] = Field(default=None)
    urls: List[Optional[str]] = Field(default=[])


class Witness(BaseModel):
    # Properties of the Witness node
    id: int
    is_unobserved: bool
    is_excerpt: bool
    siglum: Optional[str] = Field(default=None)
    alternative_sigla: List[Optional[str]] = Field(default=[])
    status: Optional[str] = Field(default=None)
    creation_date_min: Optional[date] = Field(default=None)
    creation_date_max: Optional[date] = Field(default=None)
    creation_date_year: Optional[date] = Field(default=None)
    creation_date_certainty: Optional[str] = Field(default=None)
    creation_date_text: Optional[str] = Field(default=None)
    number_of_hands: Optional[int] = Field(default=None)
    urls: List[Optional[str]] = Field(default=[])

    # Nested nodes
    scripta: Optional[Scripta] = Field(default=None)  # HasWritingStyle
    manuscripts: List[Optional[Document]] = Field(default=[])  # IsMaterializedOn
