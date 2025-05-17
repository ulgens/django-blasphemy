[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/ulgens/django-blasphemy/badge)](https://scorecard.dev/viewer/?uri=github.com/ulgens/django-blasphemy)

# django-blasphemy

Django development playground. It's for when you need to try something but the project in front of you is too complex / big / important to test stuff on it. Can be used as project starter if you have that kind of energy.

## Setup
> Make sure that you have an up to date version of Docker and `make` is installed.

* Copy `.env.dist` to `.env` and update it as you need.
* Run `make build` to build docker compose services.
* Run `make init_data` to initialize the database and create a superuser.
* Run `make up` to start the project.

The project homepage can be accessed at `http://localhost:8000/`.

# Contribution

Install pre-commit hooks by `pre-commit install`
