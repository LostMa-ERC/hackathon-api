from fastapi import APIRouter

from app.api.deps import SessionDep

router = APIRouter(
    prefix="/entities",
    tags=["entities"],
    responses={404: {"description": "Not found"}},
)


def get_table_records(
    session: SessionDep,
    table_name: str,
    primary_key: str = "H-ID",
    offset: int = 0,
    limit: int = 0,
    id: int | None = None,
):
    where_condition, limit_condition, params = None, None, None
    selection = f"SELECT * FROM {table_name}"
    if id:
        where_condition = "WHERE H-ID = ?"
        params = [id]
    order_condition = f'ORDER BY "{primary_key}"'
    if limit != 0:
        limit_condition = f"LIMIT {limit}"
    offset_condition = f"OFFSET {offset}"
    conditions = [
        selection,
        where_condition,
        order_condition,
        limit_condition,
        offset_condition,
    ]
    sql = " ".join([cond for cond in conditions if cond])
    data = session.get_dict_array(query=sql, paramaters=params)
    return data


@router.get("/language")
async def read_languages(session: SessionDep) -> list[dict]:
    """Read all the languages in the database."""
    sql = """
select * from trm where trm_ParentTermID = 9469
"""
    data = session.get_dict_array(sql)
    return data


@router.get("/storverse")
async def read_storyverses(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
) -> list[dict]:
    """Read storyverse entities."""
    data = get_table_records(
        session=session,
        table_name="Storyverse",
        offset=offset,
        limit=limit,
        id=id,
    )
    return data


@router.get("/story")
async def read_stories(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
) -> list[dict]:
    """Read story entities."""
    data = get_table_records(
        session=session, table_name="Story", offset=offset, limit=limit, id=id
    )
    return data


@router.get("/text")
async def read_texts(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
) -> list[dict]:
    """Read text entities."""
    data = get_table_records(
        session=session, table_name="TextTable", offset=offset, limit=limit, id=id
    )
    return data


@router.get("/witness")
async def read_witnesses(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
) -> list[dict]:
    """Read witness entities."""
    data = get_table_records(
        session=session, table_name="Witness", offset=offset, limit=limit, id=id
    )
    return data


@router.get("/part")
async def read_parts(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
) -> list[dict]:
    """Read part entities."""
    data = get_table_records(
        session=session, table_name="Part", offset=offset, limit=limit, id=id
    )
    return data


@router.get("/document")
async def read_documents(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
) -> list[dict]:
    """Read document entities."""
    data = get_table_records(
        session=session, table_name="DocumentTable", offset=offset, limit=limit, id=id
    )
    return data


@router.get("/repository")
async def read_repositories(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
    id: int | None = None,
) -> list[dict]:
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
