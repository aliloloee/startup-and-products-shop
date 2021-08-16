from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customUser'
    verbose_name = _('Users')
