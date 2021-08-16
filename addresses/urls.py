from django.urls import path

from . import views

app_name = 'addresses'

urlpatterns = [
    path('cities/', views.get_cities, name='cities'),
]