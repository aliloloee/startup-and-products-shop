from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.files.storage import default_storage
from django.conf import settings

from customUser.models import User

from . models import Profile



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs) :
    if created :
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Profile)
def create_user_avatar(sender, instance, *args, **kwargs) :
    new_profile = instance.avatar
    try :
        old_profile = Profile.objects.get(user=instance.user).avatar
    except :
        return

    if str(old_profile) == 'profiles/no_profile.png' :
        return

    if not new_profile == old_profile :
        media_url = settings.MEDIA_URL
        try :
            avatar = old_profile.url
            path = avatar.strip(media_url)
            default_storage.delete(path)
        except :
            pass