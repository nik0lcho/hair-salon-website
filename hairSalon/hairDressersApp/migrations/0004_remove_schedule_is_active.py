# Generated by Django 5.1.3 on 2024-12-07 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hairDressersApp', '0003_delete_deactivatetimeslots'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='is_active',
        ),
    ]
