from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.accounts_register, name='register'),
    path('verify/', views.verify_account, name='verify'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('password_reset/', views.forgotten_password, name='forgetPass'),
    path('password_reset/<token>/', views.change_forgotten_password, name='change_forgotten_password'),
    path('edit/', views.profileEdit, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'), 
]