# Generated by Django 4.1.7 on 2023-06-14 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("applications", "0004_contract"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contract",
            name="property",
        ),
        migrations.RemoveField(
            model_name="contract",
            name="user",
        ),
        migrations.AddField(
            model_name="contract",
            name="application",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="applications.application",
            ),
            preserve_default=False,
        ),
    ]
