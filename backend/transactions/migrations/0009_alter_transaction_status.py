# Generated by Django 4.1.7 on 2023-05-31 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0008_alter_transaction_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.IntegerField(
                choices=[
                    (1, "pending"),
                    (2, "paid"),
                    (3, "failed"),
                    (4, "Withdrawal approved"),
                    (5, "Withdrawal denied"),
                ],
                default=1,
            ),
        ),
    ]
