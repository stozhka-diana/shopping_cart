import pytest

from shopping_cart.services.cookies.cart_cookie_manager import CartCookieManager


class TestCartCookieManager:

    @pytest.mark.parametrize(
        'cookies, cart_id',
        [
            ({}, None),
            ({'something': 'one'}, None),
            ({'cart_id': 'long cart id'}, 'long cart id'),
        ]
    )
    def test_if_cookies_dictionary_doesnt_have_cookie_none_returned_instead_of_id(self, cookies, cart_id):
        manager = CartCookieManager(cookies)
        assert manager.get_shopping_cart_id() == cart_id

    def test_set_cart_id_creates_new_field_if_it_doesnt_exist(self):
        cart_id = 'cart id'
        manager = CartCookieManager({})
        assert not manager.get_shopping_cart_id()
        manager.set_shopping_cart_id(cart_id)
        assert manager.get_shopping_cart_id() == cart_id

    def test_set_cart_id_updates_existing_field(self):
        old_cart_id = 'old cart id'
        new_cart_id = 'new cart id'
        manager = CartCookieManager({'cart_id': old_cart_id})
        assert manager.get_shopping_cart_id() == old_cart_id
        manager.set_shopping_cart_id(new_cart_id)
        assert manager.get_shopping_cart_id() == new_cart_id
