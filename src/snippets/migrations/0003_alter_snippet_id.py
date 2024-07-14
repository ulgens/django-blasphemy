import uuid_extensions.uuid7
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("snippets", "0002_alter_snippet_language_alter_snippet_style"),
    ]

    operations = [
        migrations.AlterField(
            model_name="snippet",
            name="id",
            field=models.UUIDField(
                default=uuid_extensions.uuid7,
                editable=False,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
    ]
