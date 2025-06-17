from fastapi import APIRouter

from app.api.routes import collection, document, navigation

from .constants import DTS_COLLECTION, DTS_CONTEXT, DTS_DOCUMENT, DTS_ID, DTS_NAVIGATION

api_router = APIRouter()

# Add the API's routes
api_router.include_router(collection.router)
api_router.include_router(document.router)
api_router.include_router(navigation.router)


# At the API's main entry point, return the DTS metadata
@api_router.get("/")
async def read_index():
    """Read entry point."""
    json_ld = {
        "@context": DTS_CONTEXT,
        "@type": "EntryPoint",
        "@id": DTS_ID,
        "collection": DTS_COLLECTION,
        "document": DTS_DOCUMENT,
        "navigation": DTS_NAVIGATION,
        "dtsVersion": "unstable",
    }
    return json_ld
