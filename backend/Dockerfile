FROM python:3.12

WORKDIR /code

COPY ./pyproject.toml /code/

COPY ./src /code/src
COPY ./data /code/data

RUN pip install --upgrade pip
RUN pip install .

CMD ["fastapi", "run", "src/api/main.py", "--port", "8000"]