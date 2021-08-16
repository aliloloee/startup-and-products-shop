from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LangCtrlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lang_ctrl'
    verbose_name = _('Language Control')
