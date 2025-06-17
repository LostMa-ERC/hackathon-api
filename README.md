# Hackathon API

RESTful API prototype for the LostMa database.

## Set up 📦

1. Install Python, version 3.12 (or greater).

2. Create and activate a virtual Python environment.

3. Download the latest version of the code.

    - `git clone https://github.com/LostMa-ERC/hackathon-api.git`

    - If already downloaded, update the version with `git pull`.

4. Save Heurist sign-in credentials to a `.env` file.

    - `HEURIST_LOGIN=???`
    - `HEURIST_PASSWORD=???`

5. Install the package.

    - `pip install .`

## Launch 🚀

|Development|Production|
|--|--|
|`fastapi dev app/main.py`|`fastapi run app/main.py --host 0.0.0.0 --port 8000`|
|Reloads on saved changes.|Presents the version used at launch.|

## API entry points

Part of this API implements the [Distributed Text Services](https://distributed-text-services.github.io/specifications/) protocol, which include the entry points `collection/`, `document/`, and `navigation/`. This part is a prototype and still under development.

- [`api/v1/collection/`](http://localhost:8000/api/v1/collection)
- [`api/v1/document/`](http://localhost:8000/api/v1/document)
- [`api/v1/navigation/`](http://localhost:8000/api/v1/navigation)

The rest of the API presents data useful for the Hackathon.
