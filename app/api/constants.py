from app.core.config import settings

URL = settings.API_URL

DTS_CONTEXT = (
    "https://distributed-text-services.github.io/specifications/context/1-alpha1.json"
)

DTS_ID = f"{URL}/api/v1/dts"

DTS_COLLECTION = f"{URL}/api/v1/dts/collection" + "{?id,nav}"

DTS_DOCUMENT = f"{URL}/api/v1/dts/document" + "{?resource,ref,start,end,mediaType}"

DTS_NAVIGATION = f"{URL}/api/v1/dts/navigation" + "{?resource,ref,start,end,down,tree}"
