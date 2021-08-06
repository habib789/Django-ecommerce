from django.urls import path
from .views import (add_to_cart, CartView, Checkout,
                    remove_from_cart, reduce_from_cart, Checkout,
                    ProductDetailView, item_search, product_view)

app_name = 'products'

urlpatterns = [
    # path('', ProductView.as_view(), name='product_list'),
    path('', product_view, name='product_list'),
    path('<int:pk>/<str:p_or_c>/', product_view, name='product_list'),
    path('item_search/', item_search, name='item_search'),
    path('products/details/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('cart/<int:pk>/remove/', remove_from_cart, name='remove_from_cart'),
    path('cart/<int:pk>/reduce/', reduce_from_cart, name='reduce_from_cart'),
    path('cart/checkout/', Checkout.as_view(), name='checkout'),
]
