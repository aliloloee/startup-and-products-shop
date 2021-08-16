from django.contrib import admin

from . models import DeliveryOptions, PaymentSelection

@admin.register(DeliveryOptions)
class DeliveryOptionsAdmin(admin.ModelAdmin) :
    model = DeliveryOptions
    list_display = ('delivery_name', 'delivery_price', 'delivery_method', 'order', )

@admin.register(PaymentSelection)
class PaymentSelectionAdmin(admin.ModelAdmin) :
    model = PaymentSelection
    list_display = ('name', 'pk', )
