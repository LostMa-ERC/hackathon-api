# /api/v1/dts/collection{?id,nav}

from pydantic import BaseModel, Field


class StoryverseNode(BaseModel):
    id: int
    name: str
    alternative_names: list | None = Field(default=None)
    urls: list | None = Field(default=None)


class StoryverseCollection(BaseModel):
    storyverse: StoryverseNode
    parents: list[StoryverseNode] | None = Field(default=[])
    story_count: int
