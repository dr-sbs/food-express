# Generated by Django 3.2 on 2021-05-20 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20210501_0802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='food',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='order',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.DeleteModel(
            name='ShippingAddress',
        ),
    ]
