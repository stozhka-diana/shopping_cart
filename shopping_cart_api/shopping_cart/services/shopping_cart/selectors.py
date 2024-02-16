from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound, ValidationError as RestValidationError

from shopping_cart.models import ShoppingCart


def get_shopping_cart_by_id(shopping_cart_id: str) -> ShoppingCart:
    """
    Returns the shopping cart by its id. If none, raises exception.
    """
    try:
        return ShoppingCart.objects.get(is_ordered=False, pk=shopping_cart_id)
    except ShoppingCart.DoesNotExist:
        raise NotFound("Shopping cart with id %s doesn't exist." % shopping_cart_id)
    except (ValidationError, ValueError):
        raise RestValidationError("Your cookie with cart id %s is invalid" % shopping_cart_id)
