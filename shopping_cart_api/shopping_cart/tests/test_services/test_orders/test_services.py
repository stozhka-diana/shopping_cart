from unittest.mock import MagicMock

import pytest
from model_bakery import baker
from rest_framework.exceptions import NotFound, ValidationError

from authentication.models import CustomUser, ContactInformation
from exceptions.http_exceptions import StateConflict
from products.models import Product
from shopping_cart.models import ShoppingCart, OrderedProduct
from shopping_cart.services.cookies.services import (
    get_or_create_shopping_cart_from_cookies,
    set_shopping_cart_id_cookie
)
from shopping_cart.services.orders.services import create_new_order, OrderData, get_order_data_from_request, \
    create_ordered_product


@pytest.mark.django_db
class TestOrdersServices:

    def test_get_or_create_shopping_cart_from_cookies_returns_shopping_cart_from_cookie(self):
        shopping_cart = baker.make(ShoppingCart)
        request_cookies = {'cart_id': str(shopping_cart.pk)}
        assert get_or_create_shopping_cart_from_cookies(request_cookies) == shopping_cart

    def test_get_or_create_shopping_cart_from_cookies_creates_if_cart_id_is_wrong(self):
        request_cookies = {'cart_id': 'wrong-id'}
        shopping_cart = get_or_create_shopping_cart_from_cookies(request_cookies)
        assert isinstance(shopping_cart, ShoppingCart)
        assert request_cookies['cart_id'] != str(shopping_cart.pk)

    def test_set_shopping_cart_id_cookie_updates_cookies_dict(self):
        cookies = {}
        cart = baker.make(ShoppingCart)
        set_shopping_cart_id_cookie(cart, cookies)
        assert cookies['cart_id'] == str(cart.pk)

    def test_create_new_order_sets_cart_model_is_ordered(self, phone_number, create_product):
        cart = baker.make(ShoppingCart, is_ordered=False)
        baker.make(OrderedProduct, cart=cart, product=create_product(), quantity=1)
        assert create_new_order(cart, OrderData(customer_phone=phone_number, delivery_place='place')) == cart.order
        assert cart.is_ordered

    def test_create_order_without_products_in_cart_raises_exception(self, create_product, phone_number):
        cart = baker.make(ShoppingCart, is_ordered=False)
        with pytest.raises(ValidationError):
            create_new_order(cart, OrderData(customer_phone=phone_number, delivery_place='place'))

    def test_get_order_data_from_request_firstly_returns_data_from_body(self):
        mocked_request = MagicMock()
        request_data = {'phone_number': '+441234567890', 'location': 'NY'}
        mocked_request.data = request_data
        order_data = get_order_data_from_request(mocked_request)
        assert order_data[0]['delivery_place'] == request_data['location']
        assert order_data[0]['customer_phone'] == request_data['phone_number']

    def test_get_order_data_from_request_returns_data_from_user(self, phone_number):
        mocked_request = MagicMock()
        user = baker.make(CustomUser, contact_info=baker.make(ContactInformation, phone_number=phone_number))
        mocked_request.user = user
        mocked_request.data = None
        order_data = get_order_data_from_request(mocked_request)
        assert order_data[0]['delivery_place'] == user.contact_info.location
        assert order_data[0]['customer_phone'] == user.contact_info.phone_number

    def test_if_body_and_user_is_none_raises_exception(self):
        mocked_request = MagicMock()
        mocked_request.user.is_authenticated = False
        mocked_request.data = None
        with pytest.raises(NotFound):
            get_order_data_from_request(mocked_request)


@pytest.mark.django_db
class TestOrderedProductServices:

    def test_create_ordered_product_only_for_existing_products(self):
        assert not Product.objects.all()
        with pytest.raises(NotFound):
            create_ordered_product(baker.make(ShoppingCart), {'slug': 'some-slug', 'quantity': 12})
        assert not OrderedProduct.objects.all()

    def test_if_product_exists_ordered_product_will_be_created(self, create_product):
        product = create_product()
        created_product = create_ordered_product(
            baker.make(ShoppingCart), {'slug': product.slug, 'quantity': 12}
        )
        assert OrderedProduct.objects.first() == created_product

    def test_if_product_is_already_in_cart_exception_is_raised(self, create_product):
        product = create_product()
        cart = baker.make(ShoppingCart)
        create_ordered_product(cart, {'slug': product.slug, 'quantity': 12})
        with pytest.raises(StateConflict):
            create_ordered_product(cart, {'slug': product.slug, 'quantity': 2})
