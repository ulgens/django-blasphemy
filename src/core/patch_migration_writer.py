from django.db.migrations import writer

MIGRATION_TEMPLATE = """\
%(imports)s

class Migration(migrations.Migration):
    %(replaces_str)s%(initial_str)s%(atomic_str)s%(run_before_str)s

    dependencies = [
        %(dependencies)s\
    ]

    operations = [
        %(operations)s\
    ]
"""

writer.MIGRATION_TEMPLATE = MIGRATION_TEMPLATE
