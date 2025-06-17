from fastapi import APIRouter, HTTPException

from app.api.deps import GraphDBSessionDep
from app.models.collection import Collection, CollectionMember

router = APIRouter(
    prefix="/collection",
    tags=["collection"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_collection(
    session: GraphDBSessionDep,
    id: str | int = "Story",
    nav: str = "children",
):
    """The collection endpoint is used for navigating collections. A collection \
contains metadata for the collection itself and an array of members.

    - **id** (str|int, optional): The name of the Resource type (i.e. Story, Text) or \
the unique identifier of the Resource that can be a collection. Defaults to "Story."

    - **nav** (str, optional): Determines whether the content of the member property \
represents parent or child items. Defaults to "children."
    """

    # Test to see if the ID is a record's unique ID
    try:
        int(id)

    # If the ID is a label (can't be an integer), use it as the node label
    except Exception:
        matched_node_n = f"MATCH (n: {id})"

    # If the id is a node ID, use it in a where condition
    else:
        matched_node_n = f"MATCH (n) WHERE n.id = {id}"

    # Get the label of the node being requested
    rows = session.get_rows(query=f"{matched_node_n} RETURN n")
    if len(rows) == 0:
        return HTTPException(status_code=404, detail="No resource found.")
    for row in rows:
        node_label = row[0]["_label"]
        break

    # Get the labels for the requested node's parent and children nodes
    # TODO: Change the type of parent/child nodes based on nav?
    if node_label == "Storyverse":
        parent, child = "Storyverse", "Story"
    elif node_label == "Story":
        parent, child = "Storyverse", "Text"
    elif node_label == "Text":
        parent, child = "Story", "Witness"

    # If a collection was requested for entities other than
    # Storyverse, Story, or Text, return a 404 error
    else:
        return HTTPException(status_code=404, detail="Collection not found.")

    # Compile the query statement
    query = f"""
    {matched_node_n}
    OPTIONAL MATCH (n)-[]->(c: {child})
    OPTIONAL MATCH (p: {parent})-[]->(n)
    RETURN n, count(distinct(p)), count(distinct(c))
    ORDER BY n.id
    """

    # Compile a set of members of the collection
    members = []
    for node, parents, children in session.get_rows(query=query):
        fields = node | {"totalParents": parents, "totalChildren": children}
        collection_member = CollectionMember.model_validate(fields)
        members.append(collection_member)

    # Return a collection with the members
    return Collection(id=id, title=f"Collection of {id} entities", member=members)
