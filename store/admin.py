from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import *

admin.site.site_header = "Ecart Admin"
admin.site.index_title = "Welcome to Ecart Admin"
admin.site.site_title = "Ecart Admin"


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ["name", "slug", "is_active", "parent"]
    prepopulated_fields = {"slug": ("name",)}


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ['title', 'author', 'slug', 'price',
    #                 'in_stock', 'created_at', 'updated_at']
    # list_filter = ['in_stock', 'is_active']
    # list_editable = ['price', 'in_stock']
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    pass
