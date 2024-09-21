from django.contrib.postgres.fields import CIEmailField
from django.contrib.postgres.operations import CITextExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        CITextExtension(),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=CIEmailField(
                max_length=254,
                verbose_name="email address",
            ),
        ),
    ]
