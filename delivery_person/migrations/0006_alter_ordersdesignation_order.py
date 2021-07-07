# Generated by Django 3.2 on 2021-07-07 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_coupon'),
        ('delivery_person', '0005_remove_ordersdesignation_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersdesignation',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='designation', to='orders.order'),
        ),
    ]
