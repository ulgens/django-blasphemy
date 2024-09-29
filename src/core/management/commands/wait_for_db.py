"""
Command to wait for the database to be available before proceeding.

Inspired from https://github.com/enzofrnt/django_wait_for_db
"""

import time

import djclick as click
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.utils import OperationalError


@click.command()
def wait_for_db():
    click.secho("Waiting for the database to be available...", fg="yellow")

    while True:
        try:
            connection = connections[DEFAULT_DB_ALIAS]
            connection.ensure_connection()

            click.secho("Database available!", fg="green")

            break

        except OperationalError as e:
            click.secho(f"Error with database: {e}", fg="red")
            click.secho("Database unavailable, waiting 1 second...", fg="yellow")

            time.sleep(1)
