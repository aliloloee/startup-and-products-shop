from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'
    verbose_name = _('Checkout')
