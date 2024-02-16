# Generated by Django 4.1.3 on 2022-12-07 11:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Cart id')),
            ],
            options={
                'verbose_name': 'Shopping cart',
                'verbose_name_plural': 'Shopping carts',
            },
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='Products amount')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last updated at')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_product', to='shopping_cart.shoppingcart', verbose_name='Shopping cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_product', to='products.product', verbose_name='Product in order')),
            ],
            options={
                'verbose_name': 'Ordered product',
                'verbose_name_plural': 'Ordered products',
            },
        ),
        migrations.AddConstraint(
            model_name='orderedproduct',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gte', 1)), name='product_quantity_is_natural_int'),
        ),
    ]