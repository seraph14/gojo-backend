# Generated by Django 4.1.7 on 2023-06-02 15:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("appointments", "0002_remove_appointment_appointment_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
