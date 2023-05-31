# Generated by Django 4.1.7 on 2023-05-31 20:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0009_alter_transaction_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="payment_date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
