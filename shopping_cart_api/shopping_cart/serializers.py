from django.db.models import prefetch_related_objects, QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer

from authentication.serializers import ContactInformationSerializer
from eager_loaded_serializer.mixin import EagerLoadedSerializerMixin
from products.serializers import ProductSerializer
from shopping_cart.models import OrderedProduct, ShoppingCart, Order


class MultipleOrderedProductSerializer(ListSerializer):
    """
    The list serializer validates that slug fields are unique
    in the list of data.
    """

    def validate(self, data):
        """
        Validates that slug field is unique among list of
        data.
        """
        product_slugs = [product['slug'] for product in data]
        if len(product_slugs) != len(set(product_slugs)):
            raise ValidationError("You have duplicated product slugs.")
        return data


class SpecificOrderedProductSerializer(serializers.ModelSerializer):
    """
    Serializes specific ordered product from the shopping cart.
    """

    slug = serializers.SlugField(source='product.slug')

    class Meta:
        model = OrderedProduct
        fields = ['slug']
        list_serializer_class = MultipleOrderedProductSerializer

    def to_internal_value(self, data):
        """
        Set a `slug` field when data is deserialized.
        """
        deserialized_data = super().to_internal_value(data)
        deserialized_data['slug'] = deserialized_data.pop('product')['slug']
        return deserialized_data


class OrderedProductSerializer(SpecificOrderedProductSerializer):
    """
    The serializer for the orders with additional `quantity` field.
    """

    class Meta(SpecificOrderedProductSerializer.Meta):
        fields = SpecificOrderedProductSerializer.Meta.fields + ['quantity']


class ShoppingCartProductSerializer(serializers.ModelSerializer):
    """
    The serializer for the ordered product in the shopping cart.
    """

    product = ProductSerializer()

    class Meta:
        model = OrderedProduct
        fields = ['quantity', 'product']


class ShoppingCartSerializer(EagerLoadedSerializerMixin, serializers.ModelSerializer):
    """
    The serializer for shopping cart with list of ordered products.
    """

    ordered_products = ShoppingCartProductSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = ['pk', 'ordered_products']

    @staticmethod
    def setup_eager_loading(value: ShoppingCart, many):
        """
        Prefetches db model data to reduce the number of queries when
        a user has many ordered products.
        """
        prefetch_related_objects(
            [value], 'ordered_products__product__category__parent_category__parent_category__parent_category'
        )
        return value


class OrderInfoSerializer(ContactInformationSerializer):
    """
    The serializer for the additional information about an order.
    """

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['delivery_place'] = data.pop('location')
        data['customer_phone'] = data.pop('phone_number')
        return data


class OrderWithProductsSerializer(EagerLoadedSerializerMixin, ContactInformationSerializer):
    """
    Serializer with the order information and ordered products.
    """

    cart = ShoppingCartSerializer()

    class Meta:
        model = Order
        fields = ['pk', 'customer_phone', 'delivery_place', 'cart']

    @staticmethod
    def setup_eager_loading(value: QuerySet[Order] | Order, many: bool):
        if not many:
            ShoppingCartSerializer.setup_eager_loading(value.cart, False)
        else:
            value.select_related('cart').prefetch_related(
                'ordered_products__product__category__parent_category__parent_category__parent_category'
            )
        return value
