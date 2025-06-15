from rich import print

from app.core.db import DB
from app.models.collections import StoryverseCollection


def test_storyverse_query(db: DB):
    query = """MATCH (sv: Storyverse)
    OPTIONAL MATCH (sv)-[]->(p:Storyverse)
    OPTIONAL MATCH (s:Story)-[]->(sv)
    RETURN sv, collect(distinct(p)) as parents, count(s.id) as story_count
    ORDER BY sv.id
    """
    for sv, parents, stories in db.get_rows(query=query):
        item = StoryverseCollection(storyverse=sv, parents=parents, story_count=stories)
        print(item)
