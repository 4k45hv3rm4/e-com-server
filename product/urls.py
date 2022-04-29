from . import apis
from django.urls import path

urlpatterns = [
    path('get/list', apis.ProductListView.as_view(), name='product-list-view'),
    path('get/order/list', apis.OrderListView.as_view(), name="order-list-view"),
    path('get/cart', apis.CartView.as_view(), name="cart-view"),
    path('add/cart', apis.AddToCartView.as_view(), name="add-to-cart-view"),
    path('remove/cart', apis.CartView.as_view(), name="remove-from-cart"),
    path('post/order', apis.PlaceOrderView.as_view(), name="place-order")
]
