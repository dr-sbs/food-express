
# Generated by Django 3.2 on 2021-06-09 04:23


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_coupon_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]