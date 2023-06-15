# Generated by Django 4.1.7 on 2023-06-14 10:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0024_alter_propertyfacility_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="status",
            field=models.IntegerField(
                choices=[(0, "pending"), (1, "approved"), (2, "rejected")], default=0
            ),
        ),
    ]