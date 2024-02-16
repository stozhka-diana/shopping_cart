import pytest

from products.filters import ProductFilter


@pytest.mark.django_db
class TestProductFilter:

    def test_if_parent_category_name_is_specified_products_of_subcategory_is_returned(
            self, create_product
    ):
        created_product = create_product()
        parent_category_name = created_product.category.parent_category.name
        filtered_products = ProductFilter({'categories': parent_category_name})
        assert filtered_products.qs.first() == created_product

    def test_if_wrong_category_is_specified_none_is_returned(
            self, create_product
    ):
        created_product = create_product()
        filtered_products = ProductFilter({'categories': created_product.name + '1'})
        assert not filtered_products.qs.exists()
