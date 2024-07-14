import uuid_extensions.uuid7
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
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
