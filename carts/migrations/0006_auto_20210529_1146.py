# Generated by Django 3.0.7 on 2021-05-29 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_auto_20210523_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraddress',
            name='mobile',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
