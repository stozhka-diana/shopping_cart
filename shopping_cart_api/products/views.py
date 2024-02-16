from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from products.filters import ProductFilter
from products.serializers import TreeCategorySerializer, ProductSerializer
from products.services.selectors import get_all_root_categories, get_product_by_slug, get_all_products


class CategoriesTreeView(APIView):
    """
    Returns a list of all product categories in hierarchical
    order.
    """

    def get(self, request: Request):
        """
        Returns all categories and their descendants as list of objects.
        """
        return Response(
            TreeCategorySerializer(get_all_root_categories(), many=True, eager_loading=True).data
        )


class ProductView(GenericViewSet):
    """
    Handles the Product model.
    """

    queryset = True
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    lookup_field = 'slug'

    def retrieve(self, request: Request, slug: str):
        """
        Tries to find a specific product by its slug and returns it.
        Otherwise, a response with a 404 status code is returned.
        """
        return Response(ProductSerializer(get_product_by_slug(slug)).data)

    def list(self, request: Request):
        """
        Filters products by given conditions and returns list of them.
        If none was matched, returns an empty list.
        """
        return Response(ProductSerializer(
            self.filter_queryset(get_all_products()), many=True, eager_loading=True
        ).data)
