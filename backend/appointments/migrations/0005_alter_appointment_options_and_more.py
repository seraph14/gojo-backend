# Generated by Django 4.1.7 on 2023-06-02 15:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("appointments", "0004_alter_appointment_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="appointment",
            options={"ordering": ["-appointment_date"]},
        ),
        migrations.RemoveField(
            model_name="appointment",
            name="created_at",
        ),
    ]