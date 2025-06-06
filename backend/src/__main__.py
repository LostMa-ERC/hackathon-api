import click
import uvicorn


@click.group()
def cli():
    pass


@cli.command()
def dev():
    """Launched with `api run start` at root level"""
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8001, reload=True)


@cli.command()
def start():
    """Launched with `api run start` at root level"""
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8001, reload=False)


if __name__ == "__main__":
    cli()
