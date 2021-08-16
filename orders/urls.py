from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('order/<int:order_id>', views.order, name='order'),
    # path('set_order', views.fill_order, name='set_order'),
    path('product_details/<int:pk>/', views.product_details, name='details'),
]