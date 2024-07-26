from django.conf import settings
from django.contrib.auth import get_user_model
from djclick import command, secho
from rich.console import Console
from rich.table import Table

User = get_user_model()


def get_is_active_emoji(is_active: bool) -> str:
    return "✅" if is_active else "❌"


@command()
def list_superusers():
    """
    List all superusers in the system.
    """
    superusers = User.objects.filter(is_superuser=True)

    if not superusers.exists():
        secho("No superusers found", fg="red")
        return

    table = Table(
        row_styles=["", "dim"],
    )
    table.add_column(header="ID", style="cyan", no_wrap=True)
    table.add_column(header="email", no_wrap=True)
    table.add_column(header="is_active", justify="center")
    table.add_column(header="last_login")

    for user in superusers:
        table.add_row(
            str(user.id),
            user.email,
            get_is_active_emoji(user.is_active),
            user.last_login.strftime(settings.DATETIME_INPUT_FORMATS[0]) if user.last_login else "",
        )

    console = Console()
    console.print(table)
