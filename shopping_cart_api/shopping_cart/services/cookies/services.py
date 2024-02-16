from rest_framework.exceptions import NotFound, ValidationError

from shopping_cart.models import ShoppingCart
from shopping_cart.services.cookies.cart_cookie_manager import CartCookieManager
from shopping_cart.services.cookies.selectors import get_shopping_cart_id_from_cookies
from shopping_cart.services.shopping_cart.selectors import get_shopping_cart_by_id
from shopping_cart.services.shopping_cart.services import create_shopping_cart


def get_or_create_shopping_cart_from_cookies(cookies: dict) -> ShoppingCart:
    """
    Returns a shopping cart from the cookies. If the cookie or the
    shopping cart doesn't exist, it will create a new cart.
    """
    shopping_cart_id = get_shopping_cart_id_from_cookies(cookies)
    if not shopping_cart_id:
        return create_shopping_cart()
    try:
        return get_shopping_cart_by_id(shopping_cart_id)
    except (NotFound, ValidationError):
        return create_shopping_cart()


def set_shopping_cart_id_cookie(cart: ShoppingCart, cookies: dict):
    """
    Sets a cookie with the shopping cart id.
    """
    return CartCookieManager(cookies).set_shopping_cart_id(str(cart.pk))
