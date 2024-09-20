from django.urls import path
from .views import view_cart, add_to_cart, remove_from_cart, update_cart, checkout, order_confirmation

urlpatterns = [
    path('', view_cart, name='view-cart'),
    path('add/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
    path('update/<int:product_id>/<int:quantity>/', update_cart, name='update-cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-confirmation/', order_confirmation, name='order-confirmation'),
]
