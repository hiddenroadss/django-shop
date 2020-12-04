from django.urls import path

from store.views import ProductListView, cart_view, checkout_view, update_cart_view, process_order_view


urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('update-cart/', update_cart_view, name='update-cart'),
    path('process_order/', process_order_view, name='process-order')
]