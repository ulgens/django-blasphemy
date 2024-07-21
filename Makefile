.PHONY: help build up down manage shell bash test test_fast

ARGS := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

# Default target, display available commands
help:
	@echo "Available commands:"
	@echo "  make build"
	@echo "  make up"
	@echo "  make down"
	@echo "  make bash"
	@echo "  make manage command"
	@echo "  make shell"
	@echo "  make test [test_name]"
	@echo "  make test_fast [test_name]"

# FIXME: "ENV" doesn't sound like the best option here.
ENV = docker compose
DJANGO_ENV = $(ENV) run --rm django

build:
	${ENV} --progress plain build
up:
	${ENV} up
down:
	${ENV} down
init_data:
	${DJANGO_ENV} python manage.py init_data --dev

bash:
	${DJANGO_ENV} bash
manage:
	${DJANGO_ENV} python manage.py $(ARGS)
shell:
	${DJANGO_ENV} python manage.py shell_plus
test:
	${DJANGO_ENV} python -Wd manage.py test --parallel=auto $(ARGS)
test_fast:
	${DJANGO_ENV} python -Wd manage.py test --failfast --keepdb --parallel=auto $(ARGS)

visualize_models:
	# Requires graphviz in Dockerfile and pydot in pyproject.toml
	# Another possible renderer is pygraphviz, but it requires GCC to be installed,
	# and the result image doesn't look any different. (Can be revisited.)
	${DJANGO_ENV} python manage.py graph_models --pydot -o models.svg
