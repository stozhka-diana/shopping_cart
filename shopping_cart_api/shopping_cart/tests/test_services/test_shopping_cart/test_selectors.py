import pytest
from model_bakery import baker
from rest_framework.exceptions import NotFound, ValidationError

from shopping_cart.models import ShoppingCart
from shopping_cart.services.shopping_cart.selectors import get_shopping_cart_by_id


@pytest.mark.django_db
class TestShoppingCartSelectors:

    def test_get_shopping_cart_by_id_returns_specific_product(self):
        shopping_cart = baker.make(ShoppingCart)
        baker.make(ShoppingCart)
        assert get_shopping_cart_by_id(shopping_cart.pk) == shopping_cart

    @pytest.mark.parametrize(
        'wrong_id',
        ['wrond id', 'a1177b9e-47e8-4091-9150-446ba09b37b7']
    )
    def test_if_shopping_cart_id_is_wrong_validation_exception_is_raised(self, wrong_id):
        with pytest.raises(ValidationError):
            get_shopping_cart_by_id('wrong id')

    def test_if_shopping_cart_id_cookie_doesnt_exist_not_found_error_raises(self):
        with pytest.raises(NotFound):
            get_shopping_cart_by_id('c0cbb41a-4236-4c59-a7cf-87c2e3bacda6')
