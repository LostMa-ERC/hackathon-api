from typing import Literal

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models.entities import (Languages, Stories, Storyverses, TextItem,
                                 Texts, exclude_text_keys)

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
    format: Literal["json", "csv"] = "json",
):
    """Read storyverse entities."""
    builder = SQLBuilder(
        table_name="Storyverse", prefix="storyverse", offset=offset, limit=limit, id=id
    )
    query = builder.select_table()
    data = session.get_dict_array(query=query)
    return Storyverses(items=data)


@router.get("/story")
async def read_stories(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
    format: Literal["json", "csv"] = "json",
):
    """Read story entities."""
    builder = SQLBuilder(
        table_name="Story", prefix="story", offset=offset, limit=limit, id=id
    )
    query = builder.select_table()
    data = session.get_dict_array(query=query)
    return Stories(items=data)


@router.get("/text")
async def read_texts(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
    format: Literal["json", "csv"] = "json",
):
    """Read text entities."""
    builder = SQLBuilder(
        table_name="TextTable", prefix="text", offset=offset, limit=limit, id=id
    )
    joins = [
        Join(
            table_name="trm",
            prefix="lang",
            t0_col="language_COLUMN TRM-ID",
            on_col="trm_ID",
        ),
        Join(
            table_name="Genre",
            prefix="genre",
            t0_col="specific_genre H-ID",
            on_col="H-ID",
        ),
    ]
    query = builder.join_tables(joins=joins)
    data = session.get_dict_array(query=query)
    texts = []
    for text in data:
        text_data = {
            k.removeprefix("text_"): v for k, v in text.items() if k.startswith("text_")
        }
        language_fields = {
            k.removeprefix("lang_"): v for k, v in text.items() if k.startswith("lang_")
        }
        genre_fields = {
            k.removeprefix("genre_"): v
            for k, v in text.items()
            if k.startswith("genre_")
        }
        text_data.update({"language": language_fields, "genre": genre_fields})
        texts.append(text_data)
    if format == "json":
        return Texts(items=texts)
    else:
        return {
            "items": [
                TextItem.model_validate(d).model_dump(exclude=exclude_text_keys)
                for d in texts
            ],
            "count": len(texts),
        }


@router.get("/witness")
async def read_witnesses(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
):
    """Read witness entities."""
    builder = SQLBuilder(
        table_name="Witness", prefix="witness", offset=offset, limit=limit, id=id
    )
    query = builder.select_table()
    data = session.get_dict_array(query=query)
    return data


@router.get("/part")
async def read_parts(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
):
    """Read part entities."""
    builder = SQLBuilder(
        table_name="Part", prefix="part", offset=offset, limit=limit, id=id
    )
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
    builder = SQLBuilder(
        table_name="DocumentTable", prefix="doc", offset=offset, limit=limit, id=id
    )
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
