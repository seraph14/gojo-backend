# Generated by Django 4.1.7 on 2023-05-27 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="payment_date",
            field=models.DateTimeField(null=True),
        ),
    ]