# Generated by Django 5.1.3 on 2024-11-24 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0003_alter_profile_user_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=5),
        ),
    ]
