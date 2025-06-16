# /api/v1/dts/collection{?id,nav}

from pydantic import BaseModel, Field, computed_field


class CollectionMember(BaseModel):
    name: str = Field(serialization_alias="title")
    id: int = Field(serialization_alias="@id")
    type: str = Field(validation_alias="_label", serialization_alias="@type")
    totalParents: int
    totalChildren: int

    @computed_field
    @property
    def collection(self) -> str:
        return f"/api/dts/collection/?id={self.id}" + "{&page,nav}"


class Collection(BaseModel):
    context: str = Field(
        serialization_alias="@context",
        default="https://distributed-text-services.github.io/specifications/context/1-alpha1.json",
    )
    id: str | int = Field(serialization_alias="@id")
    type: str = Field(serialization_alias="@type", default="Collection")
    collection: str = "/api/dts/collection/{?id,page,nav}"
    dtsVersion: str = "1-alpha"
    title: str
    member: list[CollectionMember] | None = Field(defualt=[])
