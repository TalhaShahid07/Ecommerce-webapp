from django.urls import path
from .views import order_history

urlpatterns = [
    path('history/', order_history, name='order-history'),
]