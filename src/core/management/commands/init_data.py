import djclick as click
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

from users.utils import generate_readable_password

DEFAULT_EMAIL = "developer@example.com"
DEFAULT_USERNAME = "developer"

User = get_user_model()


def apply_migrations():
    response = click.prompt(
        text="\nDo you want to apply the database migrations? [Y/n]",
        type=bool,
        default=True,
        show_default=False,  # Already embedded in the text
    )

    if not response:
        return

    call_command("migrate")


def create_superuser_auto():
    does_default_user_exist = User.objects.filter(username=DEFAULT_USERNAME).exists()
    if does_default_user_exist:
        click.secho(
            f"\nUser '{DEFAULT_USERNAME}' already exists. Skipping the creation of the default superuser.",
            fg="yellow",
        )
        return

    response = click.prompt(
        text="\nDo you want to create a superuser automatically? [Y/n]",
        type=bool,
        default=True,
        show_default=False,  # Already embedded in the text
    )

    if not response:
        return

    password = generate_readable_password(acrostic="pony")

    superuser = User.objects.create_superuser(
        email=DEFAULT_EMAIL,
        username=DEFAULT_USERNAME,
        password=password,
    )

    click.secho("\nSuperuser created successfully!", fg="green")
    click.secho("New superuser details:", fg="green")
    click.secho(f"  - Username: {DEFAULT_USERNAME}", fg="green")
    click.secho(f"  - Email: {DEFAULT_EMAIL}", fg="green")
    click.secho(f"  - Password: {password}", fg="green")

    password_change_url = reverse("admin:auth_user_password_change", args=[str(superuser.id)])
    # The host is hardcoded to localhost:8000 because there is no request context available
    click.secho(f"You can change this password at http://localhost:8000{password_change_url}", fg="yellow")


def create_superuser_manual():
    response = click.prompt(
        text="\nDo you want to create a superuser manually? [y/N]",
        type=bool,
        default=False,
        show_default=False,  # Already embedded in the text
    )

    if not response:
        return

    call_command("createsuperuser", interactive=True)


@click.command()
@click.option(
    "--dev",
    is_flag=True,
    default=False,
    help="Applies migrations and creates a superuser",
)
def command(dev):
    """
    Initialize the project database and populate/fetch required data
    """

    if dev:
        apply_migrations()
        call_command("list_superusers")
        create_superuser_auto()
        create_superuser_manual()


def add_arguments(self, parser):
    parser.add_argument(
        "--dev",
        help="",
        action="store_true",
    )
