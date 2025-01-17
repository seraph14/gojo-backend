# Generated by Django 4.1.7 on 2023-05-29 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0015_remove_property_availability_property_visiting_hours"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propertylocation",
            name="latitude",
            field=models.DecimalField(decimal_places=15, max_digits=30),
        ),
        migrations.AlterField(
            model_name="propertylocation",
            name="longitude",
            field=models.DecimalField(decimal_places=15, max_digits=30),
        ),
    ]
