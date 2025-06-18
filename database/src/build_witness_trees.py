from rich.progress import (
    Progress,
    BarColumn,
    MofNCompleteColumn,
    TimeElapsedColumn,
    TextColumn,
)

import json
from database.config import GRAPH_DB_PATH

from app.fetch.witness_tree import WitnessTreeBuilder
from app.core.config import settings
from app.core.db import GraphDB


def build_witness_trees():
    dir = settings.STATIC_DIR.joinpath("resource")
    dir.mkdir(exist_ok=True)
    with (
        Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        ) as p,
        GraphDB(fp=GRAPH_DB_PATH) as db,
    ):
        total = len(db.get_rows("MATCH (w:Witness) RETURN w.id"))
        wtb = WitnessTreeBuilder(db=db)
        t = p.add_task("Building witness trees", total=total)
        for wit in wtb.iter_witnesses():
            json_str = wit.model_dump_json(exclude_unset=True, exclude_none=True)
            obj = json.loads(json_str)
            obj = {"type": "witness"} | obj
            with open(dir.joinpath(f"{wit.id}.json"), "w") as f:
                json.dump(obj=obj, fp=f, indent=4, ensure_ascii=False)
            p.advance(t)
        total_files = len([_ for _ in dir.iterdir()])
        assert total == total_files
