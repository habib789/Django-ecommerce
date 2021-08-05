from django.contrib import admin
from . models import Product, Cart, Order, Address, Category, SubCategory


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'order_address',
        'order_date',
        'order_status',
    ]
    search_fields = ['user__username', 'order_status']
    list_filter = [
        'order_status',
        'order_date']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'products', 'quantity', 'status']


class SubCategoryInline(admin.TabularInline):
    model = SubCategory


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubCategoryInline,
    ]

    class Meta:
        model = Category


class ProductInline(admin.TabularInline):
    model = Product


class SubCategoryAdmin(admin.ModelAdmin):
    inlines =[
        ProductInline
    ]

    class Meta:
        model = SubCategory


admin.site.site_header = 'GEAR BOX'
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)