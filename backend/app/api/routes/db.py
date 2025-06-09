from datetime import datetime

from fastapi import APIRouter

from app.api.deps import SessionDep

router = APIRouter(
    prefix="/db", tags=["db"], responses={404: {"description": "Not authenticated"}}
)


@router.put("/")
async def reresh_database(session: SessionDep) -> dict:
    """Recreate the database at the persistent file path.

    Returns:
        dict: Message detailing the time taken to refresh the database.
    """
    print("Refreshing...")
    start = datetime.now()
    session.refresh_data()
    end = datetime.now()
    return {
        "message": "Refreshed data.",
        "updateDuration": {"start": start, "end": end},
    }
