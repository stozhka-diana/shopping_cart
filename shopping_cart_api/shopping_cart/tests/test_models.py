from datetime import datetime, timedelta

import pytest
from django.db import IntegrityError
from model_bakery import baker

from shopping_cart.models import ShoppingCart, OrderedProduct


@pytest.mark.django_db
class TestShoppingCart:

    def test_shopping_cart_id_is_created_automatically(self):
        cart = ShoppingCart.objects.create()
        assert cart.pk is not None

    def test_if_shopping_cart_doesnt_have_products_than_last_updated_at_returns_none(self):
        cart = ShoppingCart.objects.create()
        assert cart.last_updated_at is None

    def test_last_updated_at_returns_the_latest_date(self, create_product):
        cart = ShoppingCart.objects.create()
        baker.make(
            OrderedProduct, updated_at=datetime.now() - timedelta(30), cart=cart,
            product=create_product(), quantity=2
        )
        latest_product = baker.make(OrderedProduct, cart=cart, product=create_product(), quantity=2)
        assert cart.last_updated_at == latest_product.updated_at


@pytest.mark.django_db
class TestOrderedProduct:

    @pytest.mark.parametrize(
        'quantity', [0, -5]
    )
    def test_quantity_is_must_be_greater_than_0_or_exception_is_raised(self, create_product, quantity):
        with pytest.raises(IntegrityError):
            OrderedProduct.objects.create(product=create_product(), quantity=quantity)

    def test_product_updated_at_is_optionally_argument(self, create_product):
        ordered_product = baker.make(OrderedProduct, product=create_product(), quantity=2)
        assert isinstance(ordered_product.updated_at, datetime)

    def test_two_equals_products_cant_be_in_one_cart(self, create_product):
        product = create_product()
        ordered_product = baker.make(OrderedProduct, product=product, quantity=2)
        with pytest.raises(IntegrityError):
            baker.make(OrderedProduct, product=product, cart=ordered_product.cart, quantity=2)
