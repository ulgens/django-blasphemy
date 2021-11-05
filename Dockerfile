FROM python:3.10.0-slim-buster

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
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION="1.1.8"

RUN --mount=type=cache,target=/root/.cache/pip \
	pip install "poetry==$POETRY_VERSION"

RUN mkdir /code
WORKDIR /code

COPY poetry.lock pyproject.toml /code/

# I'm not sure if this is the best way to manage venv in container.
RUN poetry config virtualenvs.create false \
  && poetry config virtualenvs.path "/root/.virtualenvs" \
  && poetry install --no-interaction --no-ansi
