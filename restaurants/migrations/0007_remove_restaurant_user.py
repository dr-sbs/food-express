# Generated by Django 3.2 on 2021-04-21 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0006_restaurant_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='user',
        ),
    ]
