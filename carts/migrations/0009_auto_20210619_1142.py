# Generated by Django 3.0.7 on 2021-06-19 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0008_auto_20210619_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='billing_address_id',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='shipping_address_id',
        ),
    ]
