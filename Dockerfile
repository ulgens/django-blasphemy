FROM python:3.12.2-slim-bullseye

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt update && \
    # There should be an upgrade step on prod. image
    apt install -y \
        # required by gitpython
        git \
        # For development purposes
        nano

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=True \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Poetry settings
ENV POETRY_VERSION="1.8.1" \
    # # When true, `poetry run` is required to run the commands relating to the venv
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1

RUN --mount=type=cache,target=/root/.cache/pip \
	pip install "poetry==$POETRY_VERSION"

RUN mkdir /code
WORKDIR /code

COPY poetry.lock pyproject.toml /code/

# TODO: Share the venv folder with the host.
RUN poetry install
