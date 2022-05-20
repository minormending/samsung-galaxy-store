FROM python:3.10-slim

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN mkdir /app
COPY pyproject.toml /app
WORKDIR /app

COPY README.md /app 
RUN mkdir /app/samsung_galaxy_store
COPY samsung_galaxy_store /app/samsung_galaxy_store
RUN poetry install --no-dev

ENTRYPOINT [ "galaxy-store-cli" ]