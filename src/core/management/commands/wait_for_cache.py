"""
Command to wait for the cache to be available before proceeding.

Inspired from https://github.com/enzofrnt/django_wait_for_db
"""

import time

import djclick as click
from django.core.cache import caches
from redis.exceptions import ConnectionError as RedisConnectionError


@click.command()
def wait_for_cache():
    click.secho("Waiting for the cache to be available...", fg="yellow")

    while True:
        try:
            cache = caches["default"]
            client = cache._cache.get_client()
            client.ping()

            click.secho("Cache available!", fg="green")

            break

        except RedisConnectionError as e:
            click.secho(f"Error with cache: {e}", fg="red")
            click.secho("Cache unavailable, waiting 1 second...", fg="yellow")

            time.sleep(1)
