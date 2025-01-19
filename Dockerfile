FROM python:3.12-slim AS base

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
    PYTHONHASHSEED=random \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    POETRY_VIRTUALENVS_CREATE=false

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

RUN apt update && apt upgrade -y && \
    apt install --no-install-recommends -y bash curl build-essential gettext libpq-dev && \
    apt purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    apt clean -y && rm -rf /var/lib/apt/lists/* && \
    pip install -U pip setuptools wheel

WORKDIR /app

COPY pyproject.toml poetry.lock entrypoint.sh ./

RUN pip3 install poetry && poetry install --no-root --no-interaction --no-ansi

RUN groupadd -g 1000 -r app && useradd -d "/app" -g app -l -r -u 1000 app && \
    chown app:app -R "/app"

USER app

ENTRYPOINT ["/app/entrypoint.sh"]
