# Generated by Django 4.1.7 on 2023-06-03 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0022_property_description"),
        ("transactions", "0014_alter_userrentedproperties_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userrentedproperties",
            name="property",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rent_histories",
                to="properties.property",
            ),
        ),
    ]
