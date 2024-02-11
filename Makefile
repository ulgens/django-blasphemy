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

ENV = docker compose
DJANGO_ENV = $(ENV) run --rm django

build:
	${ENV} build --progress plain
up:
	${ENV} up
down:
	${ENV} down

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
