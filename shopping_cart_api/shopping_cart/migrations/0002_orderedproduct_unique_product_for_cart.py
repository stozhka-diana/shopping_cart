# Generated by Django 4.1.3 on 2022-12-08 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='orderedproduct',
            constraint=models.UniqueConstraint(fields=('cart', 'product'), name='unique_product_for_cart'),
        ),
    ]