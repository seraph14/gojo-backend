# Generated by Django 4.1.7 on 2023-05-30 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0017_rename_name_propertylocation_street_favorites"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="start_date",
            field=models.DateField(default="2020-12-26"),
        ),
    ]
