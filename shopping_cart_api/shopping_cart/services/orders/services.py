from typing import TypedDict

from django.db import IntegrityError
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request

from authentication.models import CustomUser
from exceptions.http_exceptions import StateConflict
from products.services.selectors import get_product_by_slug
from shopping_cart.models import ShoppingCart, OrderedProduct, Order
from shopping_cart.serializers import OrderInfoSerializer


class OrderData(TypedDict):
    """
    Additional data for the order.
    """
    customer_phone: str
    delivery_place: str


def create_ordered_product(shopping_cart: ShoppingCart, product_info: dict) -> OrderedProduct:
    """
    Creates new ordered product and adds it to the already
    existing shopping cart. If the product is already in the
    cart, exception is raised.
    """
    product_slug = product_info['slug']
    try:
        return OrderedProduct.objects.create(
            product=get_product_by_slug(product_slug),
            cart=shopping_cart,
            quantity=product_info['quantity'],
        )
    except IntegrityError:
        raise StateConflict(
            "You already have a product with slug %s in your cart. "
            "You may update its quantity or delete it."
            % product_slug
        )


def create_new_order(cart: ShoppingCart, order_info: OrderData, customer: CustomUser = None) -> Order:
    """
    Creates new order and sets cart is ordered.
    """
    if not cart.products.exists():
        raise ValidationError("You haven't any products to order in your cart.")
    cart.is_ordered = True
    cart.save()
    return Order.objects.create(cart=cart, customer=customer, **order_info)


def get_order_data_from_request(request: Request) -> tuple[OrderData, CustomUser | None]:
    """
    Returns contact information for order from the request. Firstly,
    checks if request has a body with serialized contact info. Secondly,
    checks if the user is authenticated and returns his contact information
    if as an order data. If none, raises an exception.
    """
    user = None
    if request.user.is_authenticated:
        user = request.user
    if request.data:
        serializer = OrderInfoSerializer(data=request.data)
    elif user and user.contact_info:
        serializer = OrderInfoSerializer(data=OrderInfoSerializer(user.contact_info).data)
    else:
        raise NotFound("The order data hasn't been found.")
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data, user
