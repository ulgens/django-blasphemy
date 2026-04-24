# Adapted from
# * https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile
# * https://github.com/wemake-services/wemake-django-template/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/docker/django/Dockerfile

FROM python:3.14.4-slim-trixie@sha256:c11aee3b3cae066f55d1e9318fc812673aa6557073b0db0d792b59491b262e0c

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt update && \
    # There should be an upgrade step on prod. image
    apt install -y --no-install-recommends \
        # required by gitpython
        git \
        # graph_models command
        graphviz \
        # For development purposes
        just nano

ENV PYTHONBREAKPOINT="ipdb.set_trace" \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=True

# uv settings
# https://github.com/astral-sh/uv-docker-example/blob/main/pyproject.toml
# https://hynek.me/articles/docker-uv/

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Silence uv complaining about not being able to use hard links.
ENV UV_LINK_MODE=copy
# https://github.com/astral-sh/uv/pull/6834#issuecomment-2319253359
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV UV_PYTHON_PREFERENCE=only-system

# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
# uv version can not be defined in an environment variable,
# because COPY --from doesn't support variable expansion
# https://github.com/moby/moby/issues/34482
COPY --from=ghcr.io/astral-sh/uv:0.11.5@sha256:555ac94f9a22e656fc5f2ce5dfee13b04e94d099e46bb8dd3a73ec7263f2e484 /uv /uvx /bin/

# https://github.com/astral-sh/uv-docker-example/blob/a14ebc89e3a5e5b33131284968d8969ae054ed0d/Dockerfile#L13
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project
