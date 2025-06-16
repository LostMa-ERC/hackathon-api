from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.models.collection import CollectionMember, Collection

router = APIRouter(
    prefix="/collection",
    tags=["collection"],
    responses={404: {"description": "Not found"}},
)


class CollectionRequester:
    def __init__(self, node_label: str, session: SessionDep):
        self.node_label = node_label
        self.session = session

    def get(self, id: str | int | None) -> Collection:
        """Request a collection from the database and return valid metadata."""
        # Build the query
        query = self.build_collection_query(id=id)

        # Validate and model the metadata of the collections' members
        members = []
        for node, parents, children in self.session.get_rows(query=query):
            fields = node | {"totalParents": parents, "totalChildren": children}
            collection_member = CollectionMember.model_validate(fields)
            members.append(collection_member)

        # If requesting all the members, return a generic response
        if not id or id == "general":
            collection_title = self.build_collection_title()
            return Collection(id="general", title=collection_title, member=members)

        # If requesting a specific resource and it was found, return the collection
        elif len(members) > 0:
            member_title = members[0].name
            collection_title = self.build_collection_title(member_title=member_title)
            return Collection(id=id, title=collection_title, member=members)

        # If requesting a specific resource and it wasn't found, return a 404 error
        else:
            return HTTPException(status_code=404, detail="Item not found")

    def build_collection_title(self, member_title: str | None = None):
        if member_title:
            return f"Collection on the {self.node_label} '{member_title}'"
        else:
            return f"Collection of {self.node_label} entities."

    def build_collection_query(self, id: str | int | None) -> str:
        if id and id != "general":
            match_statement = f"MATCH (s:{self.node_label} {{id: {id}}})"
        else:
            match_statement = f"MATCH (s:{self.node_label})"

        return f"""
    {match_statement}
    OPTIONAL MATCH (s)-[]->(p:{self.node_label})
    OPTIONAL MATCH (c:{self.node_label})-[]->(s)
    RETURN s, count(p), count(c)
    ORDER BY s.id
    """


@router.get("/storyverse/")
async def read_storyverse_collection(session: SessionDep, id: str | None = None):
    """Read storyverses in the database."""
    return CollectionRequester(node_label="Storyverse", session=session).get(id=id)


@router.get("/story/")
async def read_story_collection(session: SessionDep, id: str | None = None):
    """Read stories in the database."""
    return CollectionRequester(node_label="Story", session=session).get(id=id)


@router.get("/text/")
async def read_text_collection(session: SessionDep, id: str | None = None):
    """Read stories in the database."""
    return CollectionRequester(node_label="Text", session=session).get(id=id)
