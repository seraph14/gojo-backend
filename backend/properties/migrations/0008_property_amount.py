# Generated by Django 4.1.7 on 2023-05-27 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0007_alter_propertyfacility_facility"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
    ]
