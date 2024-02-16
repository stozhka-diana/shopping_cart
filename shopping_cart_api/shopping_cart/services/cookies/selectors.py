from rest_framework.exceptions import NotFound

from shopping_cart.services.cookies.cart_cookie_manager import CartCookieManager
from shopping_cart.services.shopping_cart.selectors import get_shopping_cart_by_id


def get_shopping_cart_from_cookies(request_cookies: dict):
    """
    Returns shopping cart from cookies. If the cookie doesn't exist or
    cart id is wrong then the exception is raised.
    """
    shopping_cart_id = get_shopping_cart_id_from_cookies(request_cookies)
    if not shopping_cart_id:
        raise NotFound("You don't have a shopping cart.")
    return get_shopping_cart_by_id(shopping_cart_id)


def get_shopping_cart_id_from_cookies(request_cookies: dict):
    """
    Returns shopping cart id from request cookies. If none, returns
    None.
    """
    cart_cookie_manager = CartCookieManager(request_cookies)
    return cart_cookie_manager.get_shopping_cart_id()
