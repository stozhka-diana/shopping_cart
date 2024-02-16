from autoslug import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import ForeignKey
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    The product category model.
    """

    name = models.CharField("Category name", max_length=32, unique=True)
    parent_category = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='subcategories', verbose_name="Parent category"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        constraints = [
            models.CheckConstraint(
                check=models.Q(level__lte=2), name="depth_level_is_lte_2"
            )
        ]

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'parent_category'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The shop product model.
    """

    name = models.CharField("Product name", max_length=64)
    slug = AutoSlugField(
        "Product slug", populate_from='name', max_length=256, unique=True
    )
    description = models.TextField("Product description")
    category = ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products',
        verbose_name="Product category"
    )
    price = models.FloatField("Product price", validators=[MinValueValidator(0)])
    rating = models.FloatField("Product rating", validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
