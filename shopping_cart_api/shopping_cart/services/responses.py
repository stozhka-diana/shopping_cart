from rest_framework.response import Response

from shopping_cart.models import ShoppingCart
from shopping_cart.services.cookies.services import set_shopping_cart_id_cookie


def get_response_with_shopping_cart_cookie_id(cart: ShoppingCart, *args, **kwargs) -> Response:
    """
    Returns a response with set cart id cookie. All args and kwargs are
    passed to the response instance.
    """
    response = Response(*args, **kwargs)
    set_shopping_cart_id_cookie(cart, response.cookies)
    return response
