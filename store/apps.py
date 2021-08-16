from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    verbose_name = _('Store')

    def ready(self) :
        from . import signals
