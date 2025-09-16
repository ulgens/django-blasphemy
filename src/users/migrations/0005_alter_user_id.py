import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_user_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid7,
                editable=False,
                help_text="The unique identifier of the record, in UUIDv7 format.",
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
    ]
