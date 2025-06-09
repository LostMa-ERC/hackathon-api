from fastapi import APIRouter

from app.api.routes import db, entities, sql

api_router = APIRouter()
api_router.include_router(db.router)
api_router.include_router(entities.router)
api_router.include_router(sql.router)
