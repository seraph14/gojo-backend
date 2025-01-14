# Generated by Django 4.1.7 on 2023-06-03 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("transactions", "0013_alter_transaction_sender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userrentedproperties",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_rented_properties",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
