from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PreorderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'preorder'
    verbose_name = _('Preorder')
