import json

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import CustomUser
from products.models import Product
from shopping_cart.models import ShoppingCart, OrderedProduct


@pytest.mark.django_db
class TestShoppingCartView:

    @pytest.fixture
    def serialized_ordered_product(self, create_product):
        return self.serialize_order(create_product().slug, 2)

    @staticmethod
    def serialize_order(slug: str, quantity: int):
        return {'slug': slug, 'quantity': quantity}

    def test_if_no_shopping_cart_404_status_code_returned_for_list_shopping_cart(self, api_client):
        response = api_client.get(
            reverse('shopping_cart:cart-list'), content_type='application/json'
        )
        assert response.status_code == 404

    def test_list_shopping_cart_will_return_200_status_code_and_products(self, api_client, create_product):
        cart = baker.make(ShoppingCart)
        OrderedProduct.objects.create(product=create_product(), cart=cart, quantity=2)
        api_client.cookies['cart_id'] = str(cart.pk)
        response = api_client.get(
            reverse('shopping_cart:cart-list'), content_type='application/json'
        )
        assert response.status_code == 200
        assert response.data.keys() == {'pk', 'ordered_products'}

    def test_cookie_with_shopping_cart_id_is_created_when_post_request_is_sent(
            self, serialized_ordered_product, api_client
    ):
        response = api_client.post(
            reverse('shopping_cart:cart-list'), json.dumps(serialized_ordered_product),
            content_type='application/json'
        )
        assert response.cookies['cart_id'].value == str(ShoppingCart.objects.first().pk)

    def test_response_on_post_request_has_201_status_code_and_valid_data(
            self, serialized_ordered_product, api_client
    ):
        response = api_client.post(
            reverse('shopping_cart:cart-list'), json.dumps(serialized_ordered_product),
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.data.keys() == {'slug', 'quantity'}

    def test_post_request_create_new_records_in_db(self, api_client, serialized_ordered_product):
        response = api_client.post(
            reverse('shopping_cart:cart-list'), json.dumps(serialized_ordered_product),
            content_type='application/json'
        )
        shopping_cart = ShoppingCart.objects.get(pk=response.cookies['cart_id'].value)
        ordered_product = shopping_cart.ordered_products.get(product__slug=serialized_ordered_product['slug'])
        assert ordered_product.quantity == serialized_ordered_product['quantity']

    def test_update_product_quantity_returns_response_with_404_status_code_if_cart_doesnt_exist(
            self, api_client, serialized_ordered_product
    ):
        response = api_client.patch(
            reverse('shopping_cart:cart-products-quantity'), json.dumps([serialized_ordered_product]),
            content_type='application/json'
        )
        assert response.status_code == 404

    def test_if_send_duplicated_products_response_with_400_status_code_is_returned(
            self, api_client, serialized_ordered_product
    ):
        response = api_client.patch(
            reverse('shopping_cart:cart-products-quantity'),
            json.dumps([serialized_ordered_product, serialized_ordered_product]),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_if_send_dict_instead_of_list_response_with_status_code_400_returned(
            self, api_client, serialized_ordered_product
    ):
        response = api_client.patch(
            reverse('shopping_cart:cart-products-quantity'),
            json.dumps(serialized_ordered_product),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_patch_request_updates_products_quantity_in_cart(self, api_client, create_product):
        product_quantity = 2
        altered_product_quantity = product_quantity + 2
        ordered_product = baker.make(
            OrderedProduct, product=create_product(), quantity=product_quantity
        )
        serialized_ordered_product = self.serialize_order(
            ordered_product.product.slug, altered_product_quantity
        )
        api_client.cookies['cart_id'] = str(ordered_product.cart.pk)
        response = api_client.patch(
            reverse('shopping_cart:cart-products-quantity'),
            json.dumps([serialized_ordered_product]),
            content_type='application/json'
        )
        ordered_product.refresh_from_db()
        assert response.status_code == 200
        assert ordered_product.quantity == altered_product_quantity

    def test_updates_products_quantity_only_for_digits_greater_than_zero(self, api_client, create_product):
        ordered_product = baker.make(
            OrderedProduct, product=create_product(), quantity=1
        )
        serialized_ordered_product = self.serialize_order(
            ordered_product.product.slug, -1
        )
        api_client.cookies['cart_id'] = str(ordered_product.cart.pk)
        response = api_client.patch(
            reverse('shopping_cart:cart-products-quantity'),
            json.dumps([serialized_ordered_product]),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_delete_multiple_products_with_the_same_slug_returns_400_error(self, api_client):
        response = api_client.patch(
            reverse('shopping_cart:cart-products-quantity'),
            json.dumps([{'slug': 'slug'}, {'slug': 'slug'}]),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_delete_request_deletes_products_from_cart(self, api_client, create_product):
        ordered_product = baker.make(
            OrderedProduct, product=create_product(), quantity=1
        )
        api_client.cookies['cart_id'] = str(ordered_product.cart.pk)
        assert ordered_product.cart.products.count() == 1
        response = api_client.delete(
            reverse('shopping_cart:cart-delete-products'),
            json.dumps([{'slug': ordered_product.product.slug}]),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert isinstance(response.data, dict)
        assert response.data['amount'] == 1
        assert ordered_product.cart.products.all().count() == 0
        assert Product.objects.get(slug=ordered_product.product.slug) == ordered_product.product


@pytest.mark.django_db
class TestUserOrdersView:

    def get_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_new_order_if_no_cart_404_status_code_returned(self, api_client):
        response = api_client.post(reverse('shopping_cart:orders-list'))
        assert response.status_code == 404

    def test_if_no_ordered_products_in_cart_400_status_code_returned(self, api_client, phone_number):
        cart = baker.make(ShoppingCart)
        api_client.cookies['cart_id'] = str(cart.pk)
        response = api_client.post(
            reverse('shopping_cart:orders-list'),
            json.dumps({'location': 'NY', 'phone_number': phone_number}),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_order_set_new_cart_id_and_returns_201_status_code(self, api_client, phone_number, create_product):
        cart = baker.make(ShoppingCart)
        baker.make(OrderedProduct, cart=cart, product=create_product(), quantity=1)
        baker.make(OrderedProduct, cart=cart, product=create_product(), quantity=3)
        old_cart_id = str(cart.pk)
        api_client.cookies['cart_id'] = old_cart_id
        response = api_client.post(
            reverse('shopping_cart:orders-list'),
            json.dumps({'location': 'NY', 'phone_number': phone_number}),
            content_type='application/json'
        )
        new_cart_id = response.cookies['cart_id'].value
        assert response.status_code == 201
        assert new_cart_id != old_cart_id
        new_cart = ShoppingCart.objects.get(pk=new_cart_id)
        assert not new_cart.is_ordered

    def test_user_orders_list_returns_empty_list_if_none(self, api_client):
        user = baker.make(CustomUser)
        api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token(user))
        response = api_client.get(reverse('shopping_cart:orders-user-orders'))
        assert isinstance(response.data, list)
        assert not response.data
