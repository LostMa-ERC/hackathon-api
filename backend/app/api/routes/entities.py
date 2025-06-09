from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models.entities import Languages, Stories, Storyverses, Texts

from .utils import Join, SQLBuilder

router = APIRouter(
    prefix="/entities",
    tags=["entities"],
    responses={404: {"description": "Not found"}},
)


@router.get("/language")
async def read_languages(session: SessionDep):
    """Read all the languages in the database."""
    sql = """
select * from trm where trm_ParentTermID = 9469
"""
    data = session.get_dict_array(sql)
    return Languages(items=data)


@router.get("/storyverse")
async def read_storyverses(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
):
    """Read storyverse entities."""
    builder = SQLBuilder(table_name="Storyverse", offset=offset, limit=limit, id=id)
    query = builder.select_table()
    data = session.get_dict_array(query=query)
    return Storyverses(items=data)


@router.get("/story")
async def read_stories(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
):
    """Read story entities."""
    builder = SQLBuilder(table_name="Story", offset=offset, limit=limit, id=id)
    query = builder.select_table()
    data = session.get_dict_array(query=query)
    return Stories(items=data)


@router.get("/text")
async def read_texts(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
):
    """Read text entities."""
    builder = SQLBuilder(table_name="TextTable", offset=offset, limit=limit, id=id)
    joins = [
        Join(table_name="trm", t0_col="language_COLUMN TRM-ID", on_col="trm_ID"),
        Join(table_name="Genre", t0_col="specific_genre H-ID", on_col="H-ID"),
    ]
    query = builder.join_tables(joins=joins)
    data = session.get_dict_array(query=query)
    texts = []
    for text in data:
        text_data = {
            k.removeprefix("t0_"): v for k, v in text.items() if k.startswith("t0_")
        }
        language_fields = {
            k.removeprefix("t1_"): v for k, v in text.items() if k.startswith("t1_")
        }
        genre_fields = {
            k.removeprefix("t2_"): v for k, v in text.items() if k.startswith("t2_")
        }
        text_data.update({"language": language_fields, "genre": genre_fields})
        texts.append(text_data)
    return Texts(items=texts)


@router.get("/witness")
async def read_witnesses(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
):
    """Read witness entities."""
    builder = SQLBuilder(table_name="Witness", offset=offset, limit=limit, id=id)
    data = builder.select_table(session=session)
    return data


@router.get("/part")
async def read_parts(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
):
    """Read part entities."""
    builder = SQLBuilder(table_name="Part", offset=offset, limit=limit, id=id)
    data = builder.select_table(session=session)
    return data


@router.get("/document")
async def read_documents(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
):
    """Read document entities."""
    builder = SQLBuilder(table_name="DocumentTable", offset=offset, limit=limit, id=id)
    data = builder.select_table(session=session)
    return data


@router.get("/repository")
async def read_repositories(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
):
    sql = """
SELECT r.*, p.place_name, p.administrative_region, p.country, p.location_mappable
FROM Repository r
LEFT JOIN Place p ON r."city H-ID" = p."H-ID"
"""
    if id:
        sql += 'WHERE r."H-ID" = ?'
        params = [id]
    else:
        params = None
    sql += 'ORDER BY "H-ID"'
    if limit != 0:
        sql += f"\nLIMIT = {limit}"
    sql += f"\nOFFSET = {offset}"
    data = session.get_dict_array(query=sql, paramaters=params)
    return data
