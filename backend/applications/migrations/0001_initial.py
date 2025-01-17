# Generated by Django 4.1.7 on 2023-05-28 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("properties", "0011_rename_amount_propertyfacility_count"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("possible_start_date", models.DateField()),
                ("how_long", models.IntegerField(default=1)),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "pending"),
                            (1, "approved"),
                            (2, "withdrawn"),
                            (3, "rejected"),
                        ],
                        default=0,
                    ),
                ),
                ("description", models.TextField()),
                ("application_date", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="properties.property",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications_by_tenant",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
    ]
