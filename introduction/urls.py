from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings

from . import views


app_name = 'introduction'


urlpatterns = [
    # path('', cache_page(settings.CACHE_TTL)(views.intro), name='company'),
    path('', views.intro, name='company'),
    path('contact/', views.contact, name='contact'),
]