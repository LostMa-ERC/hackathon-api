from collections import namedtuple

from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.models.collection import Collection, CollectionMember

router = APIRouter(
    prefix="/collection",
    tags=["collection"],
    responses={404: {"description": "Not found"}},
)

Connector = namedtuple("ConnectorNodes", field_names=["parent", "child"])


@router.get("/")
async def read_collection(session: SessionDep, id: str | int):
    """Read collections of entities in the database."""
    try:
        int(id)

    # If the id is a label / can't be an integer, use it as the node label
    except Exception:
        match_statement = f"MATCH (n: {id})"

    # If the id is a node ID, use it in a where condition
    else:
        match_statement = f"MATCH (n) WHERE n.id = {id}"

    # Get the label of the node being requested
    rows = session.get_rows(query=f"{match_statement} RETURN n")
    if len(rows) == 0:
        return HTTPException(status_code=404, detail="No resource found.")
    for row in rows:
        node_label = row[0]["_label"]
        break

    # Get the labels for the requested node's parent and children nodes
    if node_label == "Storyverse":
        labels = Connector(parent="Storyverse", child="Story")
    elif node_label == "Story":
        labels = Connector(parent="Storyverse", child="Text")
    elif node_label == "Text":
        labels = Connector(parent="Story", child="Witness")
    else:
        labels = Connector(parent=node_label, child=node_label)

    # Compile the query statement
    query = f"""
    {match_statement}
    OPTIONAL MATCH (n)-[]->(c: {labels.child})
    OPTIONAL MATCH (p: {labels.parent})-[]->(n)
    RETURN n, count(distinct(p)), count(distinct(c))
    ORDER BY n.id
    """

    members = []
    for node, parents, children in session.get_rows(query=query):
        fields = node | {"totalParents": parents, "totalChildren": children}
        collection_member = CollectionMember.model_validate(fields)
        members.append(collection_member)

    return Collection(id=id, title=f"Collection of {id} entities", member=members)
