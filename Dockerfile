FROM python:3.11-slim-bullseye

WORKDIR /fiap-tech-challenge-1

RUN pip install poetry==1.8.3
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

COPY src/ /fiap-tech-challenge-1/src/

RUN poetry install --no-dev
# RUN poetry install


CMD ["uvicorn", "src.adapters.driver.entrypoints.app:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["echo", "asdasadssa"]