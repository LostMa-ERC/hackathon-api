import subprocess
from pathlib import Path

import click

from app.core.config import settings


@click.command
@click.option("--write", is_flag=True, default=False)
def run_kuzu_explorer(write: bool):
    db = Path(settings.KUZU_PATH)
    if not db.is_dir():
        raise NotADirectoryError(db)
    if write:
        command = f"""docker run -p 8000:8000 \
-v {db.absolute()}:/database \
--rm kuzudb/explorer:latest"""
    else:
        command = f"""docker run -p 8000:8000 \
-v {db.absolute()}:/database \
-e MODE=READ_ONLY \
--rm kuzudb/explorer:latest"""
    subprocess.call(command, shell=True)


if __name__ == "__main__":
    run_kuzu_explorer()
