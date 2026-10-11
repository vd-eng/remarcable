from django.contrib import admin

from .models import Category, Product, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category', 'tags')
    search_fields = ('description',)
    filter_horizontal = ('tags',)
