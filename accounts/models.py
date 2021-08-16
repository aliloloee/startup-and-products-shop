from django.db import models
from django.utils.translation import gettext_lazy as _

from customUser.models import User
from .models_utils import profile_directory_path

from django.utils import timezone

## Created and Updated missing !!!!
class Profile (models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))

    avatar = models.ImageField(upload_to=profile_directory_path, default='profiles/no_profile.png',
                                                                verbose_name=_('Profile Picture'))
    bio = models.TextField(max_length=500, blank=True, verbose_name=_('Biography'))
    company = models.TextField(max_length=500, blank=True, verbose_name=_('Company'))
    website = models.URLField(max_length=200, blank=True, verbose_name=_('Company website'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta :
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    # def filename(self):
    #     return os.path.basename(self.avatar.name)

    def __str__(self):
        return _('Profile of {}').format(self.user.username)
