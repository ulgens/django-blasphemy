import shutil
import subprocess  # noqa: S404

from django.core.management import utils

# Celery app needs to be imported for its initialization
from .celery import app as celery_app

__all__ = ("celery_app",)


def find_formatters():
    return {"ruff_path": shutil.which("ruff")}


utils.find_formatters = find_formatters


def run_formatters(written_files, ruff_path=(sentinel := object())):  # noqa: B008
    # Use a sentinel rather than None, as which() returns None when not found.
    if ruff_path is sentinel:
        ruff_path = shutil.which("ruff")

    if ruff_path:
        subprocess.run(
            [ruff_path, "check", "--force-exclude", "--fix", *written_files],  # noqa: S603
            capture_output=True,
        )
        subprocess.run(
            [ruff_path, "format", "--force-exclude", *written_files],  # noqa: S603
            capture_output=True,
        )


utils.run_formatters = run_formatters
