IN_CONTAINER := path_exists("/.dockerenv")
COMPOSE_CMD := "docker compose"
DJANGO_CMD := if IN_CONTAINER == "true" { "" } else { COMPOSE_CMD + " run --rm django" }

set working-directory := 'src/'

# List available commands
default:
    @just --list --unsorted

# Build the Docker containers
[group("compose")]
build *ARGS:
    {{ COMPOSE_CMD }} --progress plain build {{ ARGS }}

# Start the Docker containers
[group("compose")]
up *ARGS:
    {{ COMPOSE_CMD }} up {{ ARGS }}

# Stop the Docker containers
[group("compose")]
stop *ARGS:
    {{ COMPOSE_CMD }} stop {{ ARGS }}

# Open a bash shell in the Django container
[group("django")]
bash:
    {{ DJANGO_CMD }} bash

# Run a Django management command
[group("django")]
manage *ARGS:
    {{ DJANGO_CMD }} python manage.py {{ ARGS }}

# Open a shell_plus in Django container
[group("django")]
shell:
    {{ DJANGO_CMD }} python manage.py shell_plus

# Initialize the database with development data
[group("django")]
init_data:
    {{ DJANGO_CMD }} python manage.py init_data --dev

# Run Django tests
[group("django")]
test *ARGS:
    {{ DJANGO_CMD }} python -Wd manage.py test --shuffle --parallel=auto {{ ARGS }}

# Run Django tests with failfast and keepdb
[group("django")]
test_fast *ARGS:
    {{ DJANGO_CMD }} python -Wd manage.py test --failfast --keepdb --shuffle --parallel=auto {{ ARGS }}

# Generate a visual representation of the Django models
[group("visualization")]
visualize_models *ARGS:
    {{ DJANGO_CMD }} python manage.py graph_models --pydot -o models.svg {{ ARGS }}
