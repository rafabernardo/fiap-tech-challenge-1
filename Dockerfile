FROM python:3.11-slim-bullseye
# TODO verify how to add a default value
ARG API_PORT=API_PORT

WORKDIR /fiap-tech-challenge-1
RUN pip install poetry==1.8.3
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock README.md ./

COPY src/ /fiap-tech-challenge-1/src/

RUN poetry install --no-dev

#TODO verify how to run CMD as list of args
CMD uvicorn src.api.app:app --host 0.0.0.0 --port ${API_PORT}