# Generated by Django 3.0.7 on 2021-03-06 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210213_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='storage',
            field=models.IntegerField(null=True),
        ),
    ]