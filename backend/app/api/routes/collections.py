from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models.collections import StoryverseCollection

router = APIRouter(
    prefix="/collection",
    tags=["collection"],
    responses={404: {"description": "Not found"}},
)


@router.get("/storyverse/")
async def read_storyverses(session: SessionDep, id: int | None = None):
    """Read storyverses in the database."""
    where_filter = ""
    parameters = {}
    if id:
        where_filter = " {id:$id}"
        parameters = {"id": id}
    query = f"""MATCH (sv: Storyverse{where_filter})
    OPTIONAL MATCH (sv)-[]->(p:Storyverse)
    OPTIONAL MATCH (s:Story)-[]->(sv)
    RETURN sv, collect(distinct(p)) as parents, count(s.id) as story_count
    ORDER BY sv.id
    """
    results = []
    for sv, parents, stories in session.get_rows(query=query, parameters=parameters):
        item = StoryverseCollection(storyverse=sv, parents=parents, story_count=stories)
        results.append(item)
    return results
