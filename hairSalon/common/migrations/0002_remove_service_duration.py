# Generated by Django 5.1.3 on 2024-12-01 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='duration',
        ),
    ]
