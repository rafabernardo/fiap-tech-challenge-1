FROM python:3.11-slim-bullseye

RUN export PYTHONPATH="$PYTHONPATH:$PWD"


WORKDIR /fiap-tech-challenge-1

RUN pip install poetry==1.8.3
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock README.md ./

COPY src/ /fiap-tech-challenge-1/src/

RUN poetry install
# RUN poetry install
EXPOSE 8000
CMD ["uvicorn", "adapters.driver.entrypoints.app:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["echo", "asdasadssa"]