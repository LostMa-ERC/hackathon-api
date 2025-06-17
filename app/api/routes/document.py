from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep


router = APIRouter(
    prefix="/document",
    tags=["document"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_resource(
    session: SessionDep,
    resource: str,
    ref: str = None,
    start: str = None,
    end: str = None,
    tree: str = None,
    mediaType: str = None,
):
    """The Document endpoint is used to access the content of document, as opposed to \
metadata (which is found in collections).

    - **resource** (str): The unique identifier for the Resource whose tree or subtree \
must be returned.

    - **ref** (str, optional): The string identifier of a single node in the \
CitationTree for the Resource, used as the root for the sub-tree to be reconstructed. \
Defaults to None.

    - **start** (str, optional): The string identifier of a node in the CitationTree \
for the Resource, used as the starting point for a range that serves as the reference \
point for the query. This parameter is inclusive, so the starting point is considered \
part of the sub-tree to be returned. Defaults to None.

    - **end** (str, optional): The string identifier of a node in the CitationTree for \
the Resource, used as the ending point for a range that serves as the reference point \
for the query. This parameter is inclusive, so the supplied ending point is considered \
part of the specified range. Defaults to None.

    - **tree** (str, optional): The string identifier for a CitationTree of the \
Resource. Defaults to None.

    - **mediaType** (str, optional): The string identifier for the media-type the \
resource must be returned in. Defaults to None.
    """

    # This entry point isn't prepared yet
    return HTTPException(
        status_code=404,
        detail="Resource not found. Entry point under development.",
    )
