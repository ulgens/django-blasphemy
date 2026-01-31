<div align="center">

# django-blasphemy

[![Python](https://img.shields.io/badge/python-3.14-306998?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-6.0-0C4B33?&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-18-0064a5?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-ready-1D63ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![prek](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Renovate](https://img.shields.io/badge/renovate-enabled-328be4?logo=renovate)](https://github.com/renovatebot/renovate)

[![Git Hooks](https://img.shields.io/github/actions/workflow/status/ulgens/django-blasphemy/prek.yml?logo=github&label=Git%20Hooks)](https://github.com/ulgens/django-blasphemy/actions/workflows/prek.yml)
[![Tests](https://img.shields.io/github/actions/workflow/status/ulgens/django-blasphemy/tests.yml?logo=github&label=Tests)](https://github.com/ulgens/django-blasphemy/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/ulgens/django-blasphemy/graph/badge.svg?token=EBNHI3IK23)](https://codecov.io/gh/ulgens/django-blasphemy)

</div>

<!--
# They make it look too crowded. Consider enabling them later.

-->

An opinionated Django project template for experimentation and prototyping. Useful as a development playground or project starter.

## Prerequisites
- A terminal emulator.
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [just](https://just.systems/man/en/)
- [prek](https://github.com/j178/prek?tab=readme-ov-file#installation)
- [git-lfs](https://git-lfs.github.com/)
- A modern web browser.

## Setup
> Make sure that you have an up to date version of Docker and [just](https://just.systems/man/en/) is installed.

* Copy `.env.dist` to `.env` and update it as you need.
* Run `just build` to build docker compose services.
* Run `just init_data` to initialize the database and create a superuser.
* Run `just up` to start the project.

The project homepage can be accessed at `http://localhost:8000/`.

## Troubleshooting

### Git LFS
* Installation: Follow the installation steps for your OS/tooling: https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage.
* If you are having issues with LFS files, like missing file content, ensure that:
  * LFS is installed and working fine, by using `git lfs -v`.
  * Hooks are installed, by using `git lfs install`.
  * Files are pulled successfully, by using `git lfs pull`.

# Contribution
Install git hooks by `prek install`
