from modeltranslation.translator import register, TranslationOptions
from . models import DeliveryOptions, PaymentSelection


@register(DeliveryOptions)
class DeliveryOptionsTranslationOptions(TranslationOptions):
    fields = ('delivery_name','delivery_timeframe', 'delivery_window', )

@register(PaymentSelection)
class PaymentSelectionTranslationOptions(TranslationOptions):
    fields = ('name', )
