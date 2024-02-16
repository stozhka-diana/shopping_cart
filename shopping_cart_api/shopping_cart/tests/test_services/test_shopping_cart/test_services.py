import pytest
from model_bakery import baker

from products.models import Product
from shopping_cart.models import ShoppingCart, OrderedProduct
from shopping_cart.services.shopping_cart.services import (
    create_shopping_cart, update_products_quantity_in_cart, delete_products_from_shopping_cart
)


@pytest.mark.django_db
class TestShoppingCartServices:

    def test_create_shopping_cart_creates_new_record(self):
        shopping_cart = create_shopping_cart()
        assert isinstance(shopping_cart, ShoppingCart)

    def test_update_products_quantity_in_cart_affects_only_products_with_matched_slug(self, create_product):
        cart = baker.make(ShoppingCart)
        ordered_product_quantity = 1
        ordered_products = baker.make(
            OrderedProduct, cart=cart, product=lambda: create_product(),
            quantity=ordered_product_quantity, _quantity=3
        )
        serialized_ordered_products = [
            {'slug': ordered_product.product.slug + '1', 'quantity': ordered_product_quantity + 1}
            for ordered_product in ordered_products
        ]
        update_products_quantity_in_cart(cart, serialized_ordered_products)
        for product in cart.ordered_products.all():
            assert product.quantity == ordered_product_quantity

    def test_update_products_quantity_changes_their_quantity_field(self, create_product):
        cart = baker.make(ShoppingCart)
        ordered_product_quantity = 1
        altered_product_quantity = 2
        ordered_products = baker.make(
            OrderedProduct, cart=cart, product=lambda: create_product(),
            quantity=ordered_product_quantity, _quantity=3
        )
        serialized_ordered_products = [
            {'slug': ordered_product.product.slug, 'quantity': altered_product_quantity}
            for ordered_product in ordered_products
        ]
        update_products_quantity_in_cart(cart, serialized_ordered_products)
        for product in cart.ordered_products.all():
            assert product.quantity == altered_product_quantity

    def test_delete_products_from_cart_deletes_them_by_slug(self, create_product):
        cart = baker.make(ShoppingCart)
        ordered_product_amount = 2
        ordered_products = baker.make(
            OrderedProduct, cart=cart, product=lambda: create_product(),
            quantity=ordered_product_amount, _quantity=ordered_product_amount
        )
        assert cart.ordered_products.count() == ordered_product_amount
        delete_products_from_shopping_cart(cart, [{'slug': ordered_products[0].product.slug}])
        assert cart.ordered_products.count() == ordered_product_amount - 1
        assert not cart.ordered_products.filter(product__slug=ordered_products[0].product.slug).exists()
        assert Product.objects.filter(slug=ordered_products[0].product.slug).exists()
