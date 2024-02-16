from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from shopping_cart.services.cookies.selectors import get_shopping_cart_from_cookies
from shopping_cart.services.cookies.services import get_or_create_shopping_cart_from_cookies
from shopping_cart.services.orders.selectors import get_user_orders
from shopping_cart.services.responses import get_response_with_shopping_cart_cookie_id
from view_mixins.mixins.compounds import CompoundMixin
from shopping_cart.serializers import (
    OrderedProductSerializer, ShoppingCartSerializer, SpecificOrderedProductSerializer, OrderWithProductsSerializer
)
from shopping_cart.services.orders.services import (
    create_ordered_product, create_new_order, get_order_data_from_request
)
from shopping_cart.services.shopping_cart.services import (
    update_products_quantity_in_cart,
    delete_products_from_shopping_cart, create_shopping_cart
)


class ShoppingCartView(CompoundMixin, GenericViewSet):
    """
    The view for interaction with the user's shopping cart.
    """

    queryset = True
    serializer_class = {
        ('create', 'products_quantity'): OrderedProductSerializer,
        'delete_products': SpecificOrderedProductSerializer,
        'list': ShoppingCartSerializer,
    }

    def list(self, request: Request):
        """
        Returns information about shopping cart.
        """
        return Response(
            self.get_serializer(get_shopping_cart_from_cookies(request.COOKIES), eager_loading=True).data
        )

    def create(self, request: Request):
        """
        Adds product to the shopping cart. If the cart doesn't already
        exist, it will be created.
        """
        validated_data = self.get_request_data(data=request.data)
        cart = get_or_create_shopping_cart_from_cookies(request.COOKIES)
        return get_response_with_shopping_cart_cookie_id(
            cart,
            self.get_serializer(create_ordered_product(cart, validated_data)).data,
            status=201
        )

    @action(methods=['patch'], detail=False, url_path='products/quantity')
    def products_quantity(self, request: Request):
        """
        Updates products quantity in the cart. Products are found by their
        slug.
        """
        validated_data = self.get_request_data(data=request.data, many=True)
        altered_products = update_products_quantity_in_cart(
            get_shopping_cart_from_cookies(request.COOKIES),
            validated_data
        )
        return Response(self.get_serializer(altered_products, many=True).data)

    @action(methods=['delete'], detail=False, url_path='products')
    def delete_products(self, request: Request):
        """
        Deletes products from the shopping cart.
        """
        deleted_products_amount = delete_products_from_shopping_cart(
            get_shopping_cart_from_cookies(request.COOKIES),
            self.get_request_data(data=request.data, many=True)
        )
        return Response({'amount': deleted_products_amount})


class UserOrdersView(GenericViewSet):
    """
    The view class is responsible for user orders.
    """

    @action(detail=False, permission_classes=[IsAuthenticated], url_path='user')
    def user_orders(self, request: Request):
        """
        Returns the orders list of authenticated user.
        """
        return Response(
            OrderWithProductsSerializer(
                get_user_orders(request.user), eager_loading=True, many=True
            ).data
        )

    def create(self, request: Request):
        """
        Creates a new order with given additional data. After this,
        a new shopping cart will be created.
        """
        created_order = create_new_order(
            get_shopping_cart_from_cookies(request.COOKIES),
            *get_order_data_from_request(request)
        )
        return get_response_with_shopping_cart_cookie_id(
            create_shopping_cart(),
            OrderWithProductsSerializer(created_order, eager_loading=True).data,
            status=201
        )
