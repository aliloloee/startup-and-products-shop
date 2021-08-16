from django.contrib import admin

from .models import PreOrder

@admin.register(PreOrder)
class PreOrderAdmin(admin.ModelAdmin) :
    model = PreOrder
    list_display = ('phone_number', 'fullname', 'product', 'user_id',)