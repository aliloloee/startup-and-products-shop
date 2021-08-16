from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.conf import settings

from . models import Banner
from BANPars.cache_updater import updater

@receiver(pre_delete, sender=Banner, dispatch_uid='banner_delete_signal')
def log_deleted_question(sender, instance, using, **kwargs):
    media_url = settings.MEDIA_URL
    try :
        # delete media file
        banner_image = instance.image.url
        path = banner_image.strip(media_url)
        default_storage.delete(path)

        # delete template caches
        updater.clear_model_template_cache(model_name=instance.__class__.__name__)
    except :
        pass