from django.db import migrations


class Migration(migrations.Migration):
    dependencies = (("users", "0001_initial"),)

    operations = (
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ("-created_at",), "verbose_name": "user", "verbose_name_plural": "users"},
        ),
    )
