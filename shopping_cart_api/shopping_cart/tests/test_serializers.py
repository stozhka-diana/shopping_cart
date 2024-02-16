import pytest
from model_bakery import baker
from rest_framework.exceptions import ValidationError

from shopping_cart.models import OrderedProduct
from shopping_cart.serializers import OrderedProductSerializer


@pytest.mark.django_db
class TestOrderedProductSerializer:

    def test_ordered_product_is_deserialized_with_slug_field(self):
        ordered_product_data = {'slug': 'some-slug', 'quantity': 2}
        serializer = OrderedProductSerializer(data=ordered_product_data)
        assert serializer.is_valid()
        assert serializer.validated_data.keys() == {'slug', 'quantity'}

    @pytest.mark.parametrize(
        'ordered_product_data',
        [
            {'quantity': 1},
            {'slug': 'some-slug'},
            {'slug': 'some-slug', 'quantity': 0},
            {'slug': 'some-slug', 'quantity': -1},
            {},
        ]
    )
    def test_ordered_product_serializer_invalid_data_cases(self, ordered_product_data):
        with pytest.raises(ValidationError):
            OrderedProductSerializer(data=ordered_product_data).is_valid(raise_exception=True)

    def test_serialization_fetch_related_product_slug(self, create_product):
        ordered_product = baker.make(OrderedProduct, quantity=2, product=create_product())
        serializer_data = OrderedProductSerializer(ordered_product).data
        assert serializer_data.keys() == {'slug', 'quantity'}
        assert serializer_data['slug'] == ordered_product.product.slug
