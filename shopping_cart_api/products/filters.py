from django.db.models import QuerySet
from django_filters.rest_framework import FilterSet

from products.fields import CharInFilter
from products.models import Product
from products.services.selectors import get_categories_by_names


class ProductFilter(FilterSet):
    """
    Filtering multiple products by price, rating and their categories.
    """

    categories = CharInFilter(method='filter_categories')

    class Meta:
        model = Product
        fields = {
            'price': ['lte', 'lt', 'gte', 'gt', 'exact'],
            'rating': ['lte', 'lt', 'gte', 'gt', 'exact'],
        }

    def filter_categories(self, queryset: QuerySet[Product], name: str, value: list[str]):
        """
        Filters products by their category names in a case-insensitive way.
        User can pass multiple names separated by a comma.
        """
        products_ids_of_matched_categories = (get_categories_by_names(value)
                                              .get_descendants(include_self=True)
                                              .values_list('products__pk', flat=True))
        return queryset.filter(pk__in=products_ids_of_matched_categories)
