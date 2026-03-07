from django.db import migrations


class Migration(migrations.Migration):
    dependencies = (("users", "0006_user_phone_number"),)

    operations = (
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "user", "verbose_name_plural": "users"},
        ),
    )
