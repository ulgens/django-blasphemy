"""
django.core.management.utils.find_formatters and .utils.run_formatters are
patched to use ruff for formatting Django generated files, instead of black.

These patches are applied when they are imported from core.__init__ during the Django startup.
"""

import shutil
import subprocess
import sys
import traceback

from django.core.management import utils


def find_formatters() -> dict:
    """
    Find the ruff executable.
    """
    return {"ruff_path": shutil.which("ruff")}


utils.find_formatters = find_formatters


def run_formatters(
    written_files,
    ruff_path=(sentinel := object()),  # noqa: B008
    stderr=sys.stderr,
):
    """
    Run ruff on the given files.
    """
    # Use a sentinel rather than None, as which() returns None when not found.
    if ruff_path is sentinel:
        ruff_path = shutil.which("ruff")

    if not ruff_path:
        return

    try:
        subprocess.run(  # noqa: S603
            [ruff_path, "check", "--force-exclude", "--fix", *written_files],
            capture_output=True,
        )
        subprocess.run(  # noqa: S603
            [ruff_path, "format", "--force-exclude", *written_files],
            capture_output=True,
        )
    except OSError:
        stderr.write("Formatters failed to launch:")
        traceback.print_exc(file=stderr)


utils.run_formatters = run_formatters
