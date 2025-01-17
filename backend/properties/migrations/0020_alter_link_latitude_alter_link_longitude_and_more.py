# Generated by Django 4.1.7 on 2023-05-30 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0019_alter_hotspotnode_panorama"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="latitude",
            field=models.DecimalField(decimal_places=20, max_digits=30),
        ),
        migrations.AlterField(
            model_name="link",
            name="longitude",
            field=models.DecimalField(decimal_places=20, max_digits=30),
        ),
        migrations.AlterField(
            model_name="marker",
            name="latitude",
            field=models.DecimalField(decimal_places=20, max_digits=30),
        ),
        migrations.AlterField(
            model_name="marker",
            name="longitude",
            field=models.DecimalField(decimal_places=20, max_digits=30),
        ),
        migrations.AlterField(
            model_name="virtualtour",
            name="defaultViewPosition_latitude",
            field=models.DecimalField(decimal_places=20, max_digits=30),
        ),
        migrations.AlterField(
            model_name="virtualtour",
            name="defaultViewPosition_longitude",
            field=models.DecimalField(decimal_places=20, max_digits=30),
        ),
    ]
