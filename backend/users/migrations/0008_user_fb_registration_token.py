# Generated by Django 4.1.7 on 2023-05-28 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_alter_userverification_request_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="fb_registration_token",
            field=models.CharField(default="__empty__", max_length=600),
        ),
    ]
