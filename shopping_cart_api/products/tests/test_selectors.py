import pytest
from rest_framework.exceptions import NotFound

from products.services.selectors import get_all_root_categories, get_product_by_slug, get_categories_by_names, \
    get_products_by_ids


@pytest.mark.django_db
class TestCategorySelectors:

    def test_get_all_root_categories_returns_empty_queryset_if_none_exists(self):
        categories = get_all_root_categories()
        assert not categories.exists()

    def test_get_all_root_categories_returns_only_top_level_categories(self, create_category):
        top_level_category = create_category()
        subcategory = create_category(top_level_category)
        root_categories = get_all_root_categories()
        assert root_categories.exists()
        assert len(root_categories) == 1
        assert top_level_category in root_categories
        assert subcategory not in root_categories

    def test_get_categories_by_names_works_correct_with_case_insensitive_names(self, create_category):
        names_list = ['one', 'One', 'oNe', 'ONE']
        categories = [create_category(name=name) for name in names_list]
        matched_categories = get_categories_by_names(['one'])
        for initial_category in categories:
            assert initial_category in matched_categories

    def test_get_categories_by_names_may_work_with_case_sensitive_names(self, create_category):
        names_list = ['one', 'One', 'oNe', 'ONE']
        categories = [create_category(name=name) for name in names_list]
        matched_categories = get_categories_by_names(['one'], case_insensitive=False)
        assert categories[0] == matched_categories.first()


@pytest.mark.django_db
class TestProductSelectors:

    def test_get_product_by_slug_raise_404_exception_if_none_exists(self):
        with pytest.raises(NotFound) as e:
            get_product_by_slug("not-existed-slug")
        assert e.value.status_code == 404

    def test_specific_product_is_returned_by_its_slug(self, create_product):
        product = create_product()
        assert product == get_product_by_slug(product.slug)

    def test_get_products_by_ids_returns_products_only_with_specified_ids(self, create_product):
        product = create_product()
        create_product()
        assert get_products_by_ids([product.pk]).first() == product
