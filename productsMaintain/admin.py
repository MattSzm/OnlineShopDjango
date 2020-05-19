from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','slug']
    prepopulated_fields = {'slug':('title',)}

@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}

class ImageInline(admin.StackedInline):
    model = models.ImageOfProduct


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','slug','brand','available',
                    'isOnSale','price','priceOnSale']
    list_filter = ['available','isOnSale','category']
    list_editable = ['price', 'available','isOnSale',
                     'priceOnSale']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ImageInline]