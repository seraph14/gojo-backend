# Generated by Django 4.1.7 on 2023-06-14 07:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0009_accountbalance"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone_verified",
            field=models.BooleanField(default=False, verbose_name="phone verified"),
        ),
    ]