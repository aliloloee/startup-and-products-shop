from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_all, name='product_all'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
    path('feature/<pk>/', views.toggle_feature, name='feature_price'),
    path('option/<pk>/', views.toggle_option, name='option_price'),
]