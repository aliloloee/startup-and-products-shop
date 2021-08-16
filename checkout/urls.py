from django.urls import path

from . import views


app_name = 'checkout'


urlpatterns = [
    path("deliverychoices/", views.deliverychoices, name="deliverychoices"),
    path('set_order/', views.fill_order, name='set_order'),
    path('paymentselections/', views.payment_select, name='payment_selection'),
]