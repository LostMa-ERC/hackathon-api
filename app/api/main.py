from fastapi import APIRouter

from app.api.routes import collection
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(collection.router)

DTS_URL = (
    "https://distributed-text-services.github.io/specifications/context/1-alpha1.json"
)

DTS_DOCUMENT = (
    settings.API_URL + "/api/v1/dts/document{?resource,ref,start,end,mediaType}"
)

DTS_NAVIGATION = (
    settings.API_URL + "/api/v1/dts/navigation{?resource,ref,start,end,down,tree}"
)

DTS_COLLECTION = settings.API_URL + "/api/v1/dts/collection{?id,nav}"


@api_router.get("/")
async def read_index():
    """Read entry point."""
    json_ld = {
        "@context": DTS_URL,
        "@type": "EntryPoint",
        "document": DTS_DOCUMENT,
        "navigation": DTS_NAVIGATION,
        "@id": settings.API_URL + "/api/v1/dts",
        "collection": DTS_DOCUMENT,
        "dtsVersion": "unstable",
    }
    return json_ld
