from django.db.models import QuerySet

from authentication.models import CustomUser
from shopping_cart.models import Order


def get_user_orders(user: CustomUser) -> QuerySet[Order]:
    """
    Returns all orders that user has performed.
    """
    return user.orders.all()
