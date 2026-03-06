import re

import djclick as click
from django.conf import settings
from django.core.management import CommandError

from ...utils import generate_secret_key

env_path = settings.BASE_DIR.parent / ".env"


@click.command()
@click.option(
    "--length",
    default=64,
    help="Length of the generated secret key",
    type=int,
    show_default=True,
)
def refresh_secret_key(length):
    """
    Create a new random secret key and update the .env file with it.
    """
    if not env_path.exists():
        error_msg = f".env file found not at {env_path}"
        raise CommandError(error_msg)

    content = env_path.read_text()

    if not re.search(r"^SECRET_KEY=.+$", content, flags=re.MULTILINE):
        error_msg = "SECRET_KEY variable not found in .env file"
        raise CommandError(error_msg)

    new_content = re.sub(
        r"^SECRET_KEY=.+$",
        f"SECRET_KEY={generate_secret_key(length=length)}",
        content,
        flags=re.MULTILINE,
    )
    env_path.write_text(new_content)

    click.secho(f"SECRET_KEY replaced in {env_path}", fg="green")
