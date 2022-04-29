from . import models
from django.contrib import admin


@admin.register(models.ProductData)
class ProductDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'description']
    search_fields = ['id']


@admin.register(models.OrderData)
class OrderDataAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = [ 'user', 'amount']
    autocomplete_fields = ['product', 'user']
    list_select_related = [ 'user']


@admin.register(models.CartData)
class CartDataAdmin(admin.ModelAdmin):
    search_fields = ['user', ]
    list_display = ['user', ]
    list_select_related = ['user']
    autocomplete_fields = ['user', 'product']
