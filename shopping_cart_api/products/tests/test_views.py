import pytest
from django.urls import reverse
from rest_framework.response import Response

from products.models import Product


@pytest.mark.django_db
class TestCategoriesTreeView:

    def test_view_returns_empty_list_if_categories_dont_exist(self, api_client):
        response: Response = api_client.get(reverse('products:categories-list'))
        assert not response.data
        assert isinstance(response.data, list)

    def test_if_category_exists_it_will_be_in_response(self, api_client, create_category):
        category = create_category()
        response: Response = api_client.get(reverse('products:categories-list'))
        assert len(response.data) == 1
        assert response.data[0]['name'] == category.name
        assert response.data[0]['subcategories'] == []

    def test_if_category_exists_and_has_subcategories_they_will_be_in_response(self, api_client, create_category):
        root_category = create_category()
        subcategory = create_category(root_category)
        response: Response = api_client.get(reverse('products:categories-list'))
        assert response.status_code == 200
        assert response.data == [{
            "id": root_category.pk,
            "name": root_category.name,
            "subcategories": [
                {
                    "id": subcategory.pk,
                    "name": subcategory.name,
                    "subcategories": []
                }
            ]
        }]

    @pytest.mark.parametrize(
        'http_method',
        ['post', 'put', 'patch', 'delete']
    )
    def test_only_get_method_for_categories_is_available(self, api_client, http_method):
        response = getattr(api_client, http_method)(reverse('products:categories-list'))
        assert response.status_code == 405


@pytest.mark.django_db
class TestProductView:

    @staticmethod
    def serialize_product(product: Product):
        return {
            "id": product.pk,
            "slug": product.slug,
            "name": product.name,
            "categories": [
                {"id": category.pk, "name": category.name} for category in
                product.category.get_ancestors(include_self=True)
            ],
            "description": product.description,
            "price": product.price,
            "rating": product.rating,
        }

    def test_view_returns_404_status_code_if_product_doesnt_exist(self, api_client):
        response: Response = api_client.get(reverse('products:product-detail', args=['wrong-slug']))
        assert response.status_code == 404
        assert response.data.keys() == {'detail'}

    def test_view_returns_specific_product_by_slug_and_200_status_code(self, api_client, create_product):
        product = create_product()
        response: Response = api_client.get(reverse('products:product-detail', args=[product.slug]))
        assert response.status_code == 200
        assert response.data == self.serialize_product(product)

    @pytest.mark.parametrize(
        'http_method',
        ['post', 'put', 'patch', 'delete']
    )
    def test_only_get_method_for_product_detail_is_available(self, api_client, http_method, create_product):
        product = create_product()
        response = getattr(api_client, http_method)(reverse('products:product-detail', args=[product.slug]))
        assert response.status_code == 405

    def test_empty_list_of_products_are_returned_if_they_dont_exist(self, api_client):
        response = api_client.get(reverse('products:product-list'))
        assert isinstance(response.data, list)
        assert not response.data

    def test_list_of_existed_products_are_returned(self, api_client, create_product):
        products_amount = 4
        products = [self.serialize_product(create_product()) for _ in range(products_amount)]
        response = api_client.get(reverse('products:product-list'))
        for returned_product, created_product in zip(response.data, products):
            assert returned_product == created_product
