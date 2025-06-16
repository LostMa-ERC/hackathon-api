from pydantic import BaseModel, Field


class StoryverseNode(BaseModel):
    id: int
    name: str
    alternative_names: list | None = Field(default=None)
    urls: list | None = Field(default=None)
