from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep


router = APIRouter(
    prefix="/navigation",
    tags=["navigation"],
    responses={404: {"description": "Not found"}},
)


@router.get("/navigation/")
async def read_navigation(
    session: SessionDep,
    resource: str,
    page: int,
    ref: str = None,
    start: str = None,
    end: str = None,
    down: int = None,
    tree: str = None,
):
    """The Navigation endpoint provides information about a Resource's internal \
structures (e.g., book, chapter, line, etc.) and how they are referenced.

    - **resource** (str): The unique identifier for the Resource being navigated.

    - **page** (int): The number of identifying a page in paginated query results.

    - **ref** (str, optional): The string identifier of a single node in the citation \
tree for the Resource, used as the point of reference for the query. Defaults to None.

    - **start** (str, optional): The string identifier of a node in the citation tree \
for the resource, used as the starting point for a range that serves as the reference \
point for the query. This parameter is inclusive, so the starting point is considered \
part of the specified range. Defaults to None.

    - **end** (str, optional): The string identifier of a node in the citation tree \
for the resource, used as the ending point for a range of passages that serves as the \
reference point for the query. This parameter is inclusive, so the supplied ending \
point is considered part of the specified range. Defaults to None.

    - **down** (int, optional): The maximum depth of the citation subtree to be \
returned, relative to the specified ref, the deeper of the start/end CitableUnit, or \
if these are not provided relative to the root. A value of -1 indicates the bottom of \
the Resource citation tree. Defaults to none.

    - **tree** (str, optional): The string identifier for a CitationTree of the \
Resource. Defaults to None.

    """

    # This entry point isn't prepared yet
    return HTTPException(
        status_code=404,
        detail="Resource not found. Entry point under development.",
    )
