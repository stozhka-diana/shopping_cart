from django.db.models import QuerySet
from django.db.models.functions import Lower
from mptt.querysets import TreeQuerySet
from rest_framework.exceptions import NotFound

from products.models import Category, Product


def get_all_products() -> TreeQuerySet[Category]:
    """
    Returns all categories that are stored in the
    database.
    """
    return Product.objects.select_related('category').all().order_by('id')


def get_products_by_ids(product_ids: list[int]) -> QuerySet[Product]:
    """
    Returns the QuerySet of products whose ids match the given.
    """
    return Product.objects.filter(pk__in=product_ids).all()


def get_all_root_categories() -> TreeQuerySet[Category]:
    """
    Returns all root categories (Categories which don't
    have parents).
    """
    return Category.objects.filter(level=0).all()


def get_product_by_slug(slug: str) -> QuerySet[Product]:
    """
    Returns product or raise an 404 exception if it
    doesn't exist.
    """
    try:
        return Product.objects.select_related('category').get(slug=slug)
    except Product.DoesNotExist:
        raise NotFound("Product with slug '%s' doesn't exist." % slug)


def get_categories_by_names(names: list[str], case_insensitive=True) -> TreeQuerySet[Category]:
    """
    Returns categories whose names match the given. You may specify
    which way for filtering to use - case-insensitive or not.
    """
    if not case_insensitive:
        return Category.objects.filter(name__in=names)
    normalized_names = map(lambda x: x.lower(), names)
    return Category.objects.annotate(normalized_name=Lower('name')).filter(normalized_name__in=normalized_names).all()
