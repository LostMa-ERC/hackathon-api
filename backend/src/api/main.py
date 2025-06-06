from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.dependencies import SessionDep
from src.routers import entities, sql

# Create an instance of FastAPI
app = FastAPI()

# Prepare app for communicating with frontend
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Good."}


@app.put("/")
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


# Add routers in routers/ directory
app.include_router(sql.router)
app.include_router(entities.router)
