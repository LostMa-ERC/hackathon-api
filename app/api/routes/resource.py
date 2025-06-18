import json

from fastapi import APIRouter, HTTPException

from app.core.config import settings

router = APIRouter(
    prefix="/resource",
    tags=["resource"],
    responses={404: {"description": "Not found"}},
)

DIR = settings.STATIC_DIR.joinpath("resource")


@router.get("/witness")
async def read_entrypoint(id: int):
    fp = DIR.joinpath(f"{id}.json")
    if fp.is_file():
        with open(fp) as f:
            data = json.load(f)
            return data
    else:
        return HTTPException(status_code=404, detail="Resource not found")
