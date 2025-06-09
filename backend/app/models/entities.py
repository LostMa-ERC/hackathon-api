from typing import Annotated, List, Optional

from pydantic import BaseModel, BeforeValidator, Field, computed_field


def ignore_item(record: dict) -> dict | None:
    for v in record.values():
        if v is not None and v != []:
            return record


class ItemsBase(BaseModel):
    items: list[BaseModel]

    @computed_field
    @property
    def count(self) -> int:
        return len(self.items)


class LanguageItem(BaseModel):
    id: int = Field(validation_alias="trm_ID")
    label: str = Field(validation_alias="trm_Label")
    description: str | None = Field(validation_alias="trm_Description", default=None)
    code: str | None = Field(validation_alias="trm_Code", default=None)
    reference_url: str | None = Field(
        validation_alias="trm_SemanticReferenceURL", default=None
    )


class Languages(ItemsBase):
    items: list[LanguageItem]


class GenreItem(BaseModel):
    id: int = Field(validation_alias="H-ID")
    name: str = Field(validation_alias="preferred_name")
    alternative_name: List[Optional[str]] = Field(
        validation_alias="alternative_names", default=[]
    )
    parent_id: int | None = Field(validation_alias="parent_genre H-ID", default=None)
    description: str | None = Field(default=None)
    archetype: List[Optional[str]] = Field(default=[])
    reference_url: List[Optional[str]] = Field(
        validation_alias="described_at_URL", default=[]
    )


class StoryverseItem(BaseModel):
    id: int = Field(validation_alias="H-ID")
    name: str = Field(validation_alias="preferred_name")
    alternative_name: List[Optional[str]] = Field(
        validation_alias="alternative_names", default=[]
    )
    storyverse_id: List[Optional[int]] = Field(
        validation_alias="member_of_cycle H-ID", default=[]
    )
    reference_url: List[Optional[str]] = Field(
        validation_alias="described_at_URL", default=[]
    )


class Storyverses(ItemsBase):
    items: list[StoryverseItem]


class StoryItem(BaseModel):
    id: int = Field(validation_alias="H-ID")
    name: str = Field(validation_alias="preferred_name")
    alternative_name: list[str] = Field(
        validation_alias="alternative_names", default=[]
    )
    storyverse_id: list[int] = Field(
        validation_alias="is_part_of_storyverse H-ID", default=[]
    )
    matter: str | None = Field(default=[])
    peripheral: str | None = Field(default=None)
    model_id: list[int] = Field(validation_alias="is_modeled_on H-ID", default=[])
    reference_url: list[str] = Field(validation_alias="described_at_URL", default=[])


class Stories(ItemsBase):
    items: list[StoryItem]


class TextItem(BaseModel):
    id: int = Field(validation_alias="H-ID")
    name: str = Field(validation_alias="preferred_name")
    alternative_name: List[Optional[str]] = Field(
        validation_alias="alternative_names", default=[]
    )
    language: Annotated[LanguageItem | None, BeforeValidator(ignore_item)]
    literary_form: str | None = Field(default=None)
    is_hypothetical: str | None = Field(default=None)
    claim_freetext: str | None = Field(default=None)
    peripheral: str | None = Field(default=None)
    genre: Annotated[GenreItem | None, BeforeValidator(ignore_item)]
    length: int | None = Field(default=None)
    length_freetext: str | None = Field(default=None)
    verse_type: List[Optional[str]] = Field(default=None)
    rhyme_type: List[Optional[str]] = Field(default=None)
    stanza_type: Optional[str] = Field(validation_alias="Stanza_type", default=None)
    is_derived_from: List[Optional[int]] = Field(
        validation_alias="is_derived_from H-ID", default=[]
    )
    status: str | None = Field(validation_alias="tradition_status", default=None)
    in_stemma: List[Optional[int]] = Field(
        validation_alias="in_stemma H-ID", default=[]
    )
    has_lost_older_version: str | None = Field(default=None)
    ancient_translations_freetext: List[Optional[str]] = Field(default=None)
    rewritings_freetext: List[Optional[str]] = Field(default=None)
    note: str | None = Field(default=None)
    # Scripta -> scripta
    date: dict | None = Field(validation_alias="date_of_creation", default=None)
    date_certainty: str | None = Field(
        validation_alias="date_of_creation_certainty", default=None
    )
    date_source: str | None = Field(
        validation_alias="date_of_creation_source", default=None
    )
    date_freetext: str | None = Field(validation_alias="date_freetext", default=None)
    # Place -> place
    # Person -> author
    # Person -> adaptor
    author_freetext: str | None = Field(default=None)
    reference_url: List[Optional[str]] = Field(
        validation_alias="described_at_URL", default=[]
    )


class Texts(ItemsBase):
    items: List[TextItem]
