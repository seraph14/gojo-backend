# Generated by Django 4.1.7 on 2023-05-31 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_alter_application_property'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ['application_date']},
        ),
    ]
