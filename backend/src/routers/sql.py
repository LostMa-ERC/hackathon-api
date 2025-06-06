from fastapi import APIRouter

from src.dependencies import SessionDep

router = APIRouter(
    prefix="/sql",
    tags=["sql"],
    responses={404: {"description": "Not found"}},
)


@router.get("/physdesc")
async def read_physdesc(session: SessionDep, lang: int | None = None) -> list[dict]:
    """Read pairs of physical descriptions and parts of witnesses, if the latter's
    part has a physical description. If a language is provided, only return those
    related to witnesses that manifest a text of the provided language.

    Args:
        lang (int | None, optional): Term ID of the text's language. Defaults to None.

    Returns:
        list[dict]: Set of pairs of parts and its physical description.
    """
    from src.sql.scripts import PHYSDESC_LANG_SQL, PHYSDESC_SQL

    if not lang:
        data = session.get_dict_array(query=PHYSDESC_SQL)
    else:
        data = session.get_dict_array(query=PHYSDESC_LANG_SQL, paramaters=[lang])
    return data
