from collections.abc import Iterable
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name


class ProductQuerySet(models.QuerySet):
    """
    Adds custom filters on a product queryset to enable:

    - search on description
    - filter by category
    - filter by tags
    """
    def search(self, what: str|None) -> 'ProductQuerySet':
        if not what:
            return self
        return self.filter(description__icontains=what)

    def of_category(self, category_id: int|None) -> 'ProductQuerySet':
        if category_id is None:
            return self
        return self.filter(category_id=category_id)

    def assigned_tags(self, tag_ids: Iterable[int]) -> 'ProductQuerySet':
        if not tag_ids:
            return self
        return self.filter(tags__in=tag_ids).distinct()


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # Stops a category from being deleted if products still use it
        related_name='products'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='products',
        blank=True
    )

    objects = ProductQuerySet.as_manager()  # Use custom manager with custom filters

    def __str__(self) -> str:
        return self.name
