from django.contrib import admin

from shopping_cart.models import ShoppingCart, OrderedProduct


@admin.register(OrderedProduct)
class OrderedProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'updated_at', 'cart']


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_updated_at']
