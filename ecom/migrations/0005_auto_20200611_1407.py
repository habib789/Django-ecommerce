# Generated by Django 2.2.5 on 2020-06-11 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0004_auto_20200610_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cart_products',
            field=models.ManyToManyField(related_name='cart', to='ecom.Cart'),
        ),
    ]
