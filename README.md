[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/ulgens/django-blasphemy/badge)](https://scorecard.dev/viewer/?uri=github.com/ulgens/django-blasphemy)

# django-blasphemy

Django development playground. It's for when you need to try something but the project in front of you is too complex / big / important to test stuff on it. Can be used as project starter if you have that kind of energy.

## Prerequisites
- [git-lfs](https://git-lfs.github.com/) Ensure you follow the installation steps for your OS/tooling: https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage. If you encounter any issues with the LFS setup, make sure that:
  - It is installed and working fine, by using `git lfs -v`.
  - Hooks are installed, by using `git lfs install`.
  - Files are pulled successfully, by using `git lfs pull`.

## Setup
> Make sure that you have an up to date version of Docker and [just](https://just.systems/man/en/) is installed.

* Copy `.env.dist` to `.env` and update it as you need.
* Run `just build` to build docker compose services.
* Run `just init_data` to initialize the database and create a superuser.
* Run `just up` to start the project.

The project homepage can be accessed at `http://localhost:8000/`.

# Contribution

Install pre-commit hooks by `pre-commit install`
