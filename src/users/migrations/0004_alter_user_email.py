from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_ci_collation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                db_collation="case_insensitive",
                max_length=254,
                unique=True,
                verbose_name="email address",
            ),
        ),
    ]
