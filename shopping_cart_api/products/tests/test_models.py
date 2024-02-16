import pytest
from django.db import IntegrityError, transaction

from products.models import Category, Product


@pytest.mark.django_db
class TestCategoryModel:

    def test_category_can_be_created(self, create_category):
        create_category()
        assert Category.objects.count() == 1

    def test_category_can_have_subcategories(self, create_category):
        parent_category: Category = create_category()
        categories_amount = 5
        subcategories = [create_category(parent_category) for _ in range(categories_amount)]
        assert Category.objects.count() == categories_amount + 1
        for category in subcategories:
            assert category in parent_category.subcategories.all()

    def test_category_can_have_parent_category(self, create_category):
        parent_category: Category = create_category()
        subcategory: Category = create_category(parent_category)
        assert Category.objects.all().count() == 2
        assert subcategory.parent_category == parent_category

    def test_max_category_level_depth_is_lower_than_2(self, create_category):
        category = None
        for _ in range(3):
            category = (
                create_category(category) if category
                else create_category()
            )
        with pytest.raises(IntegrityError):
            create_category(category)


@pytest.mark.django_db
class TestProductModel:

    @pytest.fixture
    def product_data(self):
        return {
            'name': 'Book',
            'description': 'Some interesting book',
            'price': 500,
            'rating': 5,
        }

    def test_product_can_be_created(self, create_product):
        create_product()
        assert Product.objects.count() == 1

    def test_product_has_auto_generated_slug(self, product_data, create_product):
        product = create_product(**product_data)
        assert product.slug == product.name.lower()

    def test_product_has_unique_auto_generated_slug(self, product_data, create_product):
        products = [create_product(**product_data) for _ in range(2)]
        assert all(products)
        assert products[0].slug != products[1].slug

    def test_product_has_category_level_greater_than_0(self, create_nested_category, product_data):
        with pytest.raises(IntegrityError), transaction.atomic():
            Product.objects.create(**product_data, category=create_nested_category(0))
        assert not Product.objects.count()
        category = create_nested_category(2)
        product = Product.objects.create(**product_data, category=category)
        assert Product.objects.count() == 1
        assert product.category == category

    def test_product_slug_can_be_created_from_unicode_letters(self, create_product):
        assert create_product(name='тестовый продукт').slug == 'testovyi-produkt'
