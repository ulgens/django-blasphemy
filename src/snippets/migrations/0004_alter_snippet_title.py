from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("snippets", "0003_alter_snippet_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="snippet",
            name="title",
            field=models.CharField(max_length=128),
        ),
    ]
