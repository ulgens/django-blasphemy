# Adapted from
# * https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile
# * https://github.com/wemake-services/wemake-django-template/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/docker/django/Dockerfile

FROM python:3.13.5-slim-bookworm@sha256:4c2cf9917bd1cbacc5e9b07320025bdb7cdf2df7b0ceaccb55e9dd7e30987419

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt update && \
    # There should be an upgrade step on prod. image
    apt install -y --no-install-recommends \
        # required by gitpython
        git \
        # graph_models command
        graphviz \
        # For development purposes
        curl nano

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
COPY --from=ghcr.io/astral-sh/uv:0.8.6@sha256:6d9911b9f5703ed5f570d8032f2bfacc524e12f77d88e1e8f39eec742811a983 /uv /uvx /bin/

# https://github.com/astral-sh/uv-docker-example/blob/a14ebc89e3a5e5b33131284968d8969ae054ed0d/Dockerfile#L13
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV JUST_VERSION=1.40.0
ENV JUST_INSTALLER_URL="https://raw.githubusercontent.com/casey/just/3884a4e68395b46c4b3eed694b09955f65b79fcc/www/install.sh"
ADD --checksum=sha256:2f811850e7833bf2191df55683f861d09b8a9cd2d1aac5f2adff597b3d675aa4 ${JUST_INSTALLER_URL} install.sh
RUN chmod +x install.sh && ./install.sh --tag ${JUST_VERSION} --to /usr/local/bin
RUN just --completions bash > ~/.bashrc
