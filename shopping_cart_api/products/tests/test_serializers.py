import pytest

from products.serializers import TreeCategorySerializer, ProductSerializer


@pytest.mark.django_db
class TestCategorySerializer:

    def test_category_can_be_serialized(self, create_category):
        root_category = create_category()
        serialized_category = TreeCategorySerializer(root_category).data
        assert serialized_category['name'] == root_category.name
        assert serialized_category['subcategories'] == []

    def test_category_with_subcategories_can_be_serialized(self, create_category):
        root_category = create_category()
        subcategory = create_category(root_category)
        serialized_category = TreeCategorySerializer(root_category).data
        assert serialized_category['name'] == root_category.name
        assert len(serialized_category['subcategories']) == 1
        assert serialized_category['subcategories'][0]['name'] == subcategory.name
        assert serialized_category['subcategories'][0]['subcategories'] == []

    def test_category_serializer_has_valid_keys(self, create_category):
        root_category = create_category()
        serialized_category = TreeCategorySerializer(root_category).data
        assert set(serialized_category.keys()) == {'id', 'name', 'subcategories'}


@pytest.mark.django_db
class TestProductSerializer:

    def test_product_can_be_serialized(self, create_product):
        product = create_product()
        serializer = ProductSerializer(product)
        serializer_data = serializer.data
        assert serializer_data.keys() == {'id', 'slug', 'name', 'categories', 'description', 'price', 'rating'}

    def test_product_is_correctly_deserialized(self):
        product_data = {
            'name': 'Product',
            'description': 'some product',
            'price': 500,
            'rating': 4.3
        }
        serializer = ProductSerializer(data=product_data)
        assert serializer.is_valid()
