from importlib import import_module

import djclick as click
from django.conf import settings
from django.contrib.admindocs.views import (
    extract_views_from_urlpatterns,
    simplify_regex,
)
from django.core.management import CommandError
from rich import box
from rich.console import Console
from rich.table import Table


@click.command()
@click.option(
    "--unsorted",
    "-u",
    default=False,
    help="Show URLs without sorting them alphabetically",
    is_flag=True,
    type=bool,
)
@click.option(
    "--prefix",
    "-p",
    "prefixes",
    help="Filter URLs by the given prefix",
    multiple=True,
    type=str,
)
def list_urls(unsorted: bool, prefixes: list):
    """
    List URL patterns in the project with optional filtering by prefixes.
    """
    # Get URL patterns
    url_patterns = get_url_patterns(prefixes=prefixes)

    if not url_patterns:
        msg = "There are no URL patterns that match given prefixes"
        raise CommandError(msg)

    # Apply sorting
    if not unsorted:
        url_patterns.sort()

    # Create the table
    table = Table(
        box=box.ROUNDED,
        row_styles=["none", "bold"],
    )
    table.add_column(
        header="Path",
        no_wrap=True,
    )
    table.add_column(
        header="View",
        no_wrap=True,
    )
    table.add_column(
        header="Name",
        no_wrap=True,
    )

    # Fill the table
    for path, view, name in url_patterns:
        # Apply partial color to the view
        module_path, module_name = view.rsplit(".", 1)
        view = f"{module_path}.[yellow]{module_name}[/yellow]"

        # Apply partial color to the name
        if name:
            namespace, name = name.rsplit(":", 1) if ":" in name else ("", name)
            name = f"{namespace}:[red]{name}[/red]"

        table.add_row(path, view, name)

    # Show the table
    console = Console()
    console.print(table)


def get_url_patterns(prefixes=None):
    """
    Returns a list of URL patterns in the project with given prefixes.

    Each object in the returned list is a 3-tuple:
    (path, view_name, name)
    """

    url_patterns = []
    urlconf = import_module(settings.ROOT_URLCONF)

    for view_func, regex, namespace_list, name in extract_views_from_urlpatterns(urlconf.urlpatterns):
        # Path
        path = simplify_regex(regex)

        # Filter out when prefixes given but there is no prefix match
        if prefixes:
            matching_prefixes = [p for p in prefixes if path.startswith(p)]

            if not matching_prefixes:
                continue

        # View name
        view_name = "{}.{}".format(
            view_func.__module__,
            getattr(view_func, "__name__", view_func.__class__.__name__),
        )

        # URL name
        namespace = ""

        if namespace_list:
            for part in namespace_list:
                namespace += part + ":"

        name = namespace + name if name else None
        name = name or ""

        # Append to the list
        url_patterns.append((path, view_name, name))

    return url_patterns
