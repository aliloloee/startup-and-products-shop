from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _



class IntroductionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'introduction'
    verbose_name =_('Introduction')

    def ready(self) :
        from . import signals

