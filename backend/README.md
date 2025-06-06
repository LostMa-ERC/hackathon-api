# Backend

This template comes with a data file in [`data/`](data/singers.csv) and a Python package in [`src/api`](./src/api/), which is installed via the [`pyproject.toml`](./pyproject.toml) file.

## Table of contents

- [Explanation](#explanation)
- [Installation](#installation)
- [Run server](#run-development-server)
- [Testing](#testing)

## Explanation

The data is loaded into a `DuckDB` database connection when the application starts up, as seen in the [`src/api/main.py`](./src/api/main.py) module. The data is transformed into a table named "singers," and each row represents metadata about a historic opera singer.

This template's only route is `/`, from which it serves all the data it loaded into the table "singers".

Begin developping by changing the data, adding more routes, etc.

## Installation

1. Create a virtual Python environment with a version of Python 3.12 or greater.

2. Activate the environment.

3. Install the backend's requirements with `pip install -e .["dev"]`

## Run development server

Run the backend with `fastapi dev app/main.py --port 8000`.

```console
$ fastapi dev src/api/main.py --port 8000

   FastAPI   Starting development server 🚀

             Searching for package file structure from directories with __init__.py
             files
             Importing from
             /home/user/Dev/full-stack-container-example/backend/src

    module   📁 api
             ├── 🐍 __init__.py
             └── 🐍 main.py

      code   Importing the FastAPI app object from the module with the following
             code:

             from api.main import app

       app   Using import string: api.main:app

    server   Server started at http://127.0.0.1:8000
    server   Documentation at http://127.0.0.1:8000/docs
```

## Testing

Unit tests are written in the [`tests/`](./tests/) folder and tested modules are imported thanks to the fact that this project is installable as a package ([`pyproject.toml`](./pyproject.toml)).

An example test has been written using the `TestClient` of `FastAPI`. Run this example with `pytest`.

```console
$ pytest
====================== test session starts ======================
platform linux -- Python 3.12.2, pytest-8.3.5, pluggy-1.5.0
rootdir: /home/kchrist/Dev/full-stack-container-example/backend
configfile: pyproject.toml
plugins: anyio-4.9.0
collected 1 item

tests/test_get_index.py .                                   [100%]
```
