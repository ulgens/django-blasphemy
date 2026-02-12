from io import StringIO

from django.core.management import call_command

from core.testcases import TestCase


# Thanks to https://adamj.eu/tech/2024/06/23/django-test-pending-migrations/
class PendingMigrationsTests(TestCase):
    def test_no_pending_migrations(self):
        out = StringIO()

        try:
            call_command("makemigrations", "--check", stdout=out)
        except SystemExit:
            raise AssertionError("Pending migrations:\n" + out.getvalue()) from None
