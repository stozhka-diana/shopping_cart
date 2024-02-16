import pytest
from model_bakery import baker
from rest_framework.exceptions import NotFound

from shopping_cart.models import ShoppingCart
from shopping_cart.services.cookies.selectors import get_shopping_cart_from_cookies


@pytest.mark.django_db
class TestCookiesSelectors:

    def test_if_not_shopping_cart_id_in_cookies_raises_not_found_exception(self):
        with pytest.raises(NotFound):
            get_shopping_cart_from_cookies({})

    def test_if_shopping_cart_id_in_cookies_it_will_be_returned(self):
        cart = baker.make(ShoppingCart)
        assert get_shopping_cart_from_cookies({'cart_id': cart.pk}) == cart
