from django.db import models
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

from persian_tools import phone_number
from . models_utils import *
from BANPars.cache_updater import updater



class Banner (models.Model) :
    title = models.CharField(verbose_name=_('Banner title'), max_length=50)
    image = models.ImageField(upload_to=banner_directory_path, verbose_name=_('Image'))
    description = models.TextField(max_length=400, verbose_name=_('Banner description'), help_text=_('Banner description better not get too long ... '))

    slug = models.SlugField(max_length=250, blank=True, verbose_name=_('Slug'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta :
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
        ordering = ('created',)

    # def get_absolute_url(self) :
    #     return reverse('interface:patient_info', kwargs={'pk':self.pk, 'slug':self.slug})

    def save(self, *args, **kwargs):
        updater.clear_model_template_cache(model_name=Banner.__name__)
        self.slug = slugify(self.title)
        super(Banner, self).save(*args, **kwargs)

    def __str__(self) :
        return f'{self.title}'



class Service (models.Model) :
    title = models.CharField(verbose_name=_('Service title'), max_length=100)
    description = models.TextField(verbose_name=_('Service description'))
    clip = FileFieldRestricted(upload_to=clip_directory_path, blank=True)

    slug = models.SlugField(max_length=250, blank=True, verbose_name=_('Slug'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta :
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ('created',)

    # def get_absolute_url(self) :
    #     return reverse('interface:patient_info', kwargs={'pk':self.pk, 'slug':self.slug})

    def save(self, *args, **kwargs):
        updater.clear_model_template_cache(model_name=Service.__name__)
        self.slug = slugify(self.title)
        super(Service, self).save(*args, **kwargs)

    def __str__(self) :
        return f'{self.title}'


class Benefit(models.Model) :
    title = models.CharField(verbose_name=_('Benefit title'), max_length=100)
    image = models.ImageField(upload_to=benefir_directory_path, verbose_name=_('Image'))
    description = models.TextField(verbose_name=_('Benefit description'))

    slug = models.SlugField(max_length=250, blank=True, verbose_name=_('Slug'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta :
        verbose_name = _('Benefit')
        verbose_name_plural = _('Benefits')
        ordering = ('created',)

    # def get_absolute_url(self) :
    #     return reverse('interface:patient_info', kwargs={'pk':self.pk, 'slug':self.slug})

    def save(self, *args, **kwargs):
        updater.clear_model_template_cache(model_name=Benefit.__name__)
        self.slug = slugify(self.title)
        super(Benefit, self).save(*args, **kwargs)

    def __str__(self) :
        return f'{self.title}'

class TeamMember(models.Model) :
    image = models.ImageField(upload_to=team_member_directory_path, verbose_name=_('Image'))

    introduction = models.TextField(verbose_name=_('Introduction'))
    fullname = models.CharField(verbose_name=_('Fullname'), max_length=100)
    role = models.CharField(verbose_name=_('Role in team'), max_length=50)

    slug = models.SlugField(max_length=250, blank=True, verbose_name=_('Slug'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta :
        verbose_name = _('Team member')
        verbose_name_plural = _('Team members')
        ordering = ('created',)

    # def get_absolute_url(self) :
    #     return reverse('interface:patient_info', kwargs={'pk':self.pk, 'slug':self.slug})

    def save(self, *args, **kwargs):
        updater.clear_model_template_cache(model_name=TeamMember.__name__)
        self.slug = slugify(self.fullname)
        super(TeamMember, self).save(*args, **kwargs)

    def __str__(self) :
        return f'{self.fullname}'

class Contact(models.Model) :
    fullname = models.CharField(verbose_name=_('Fullname'), max_length=100)
    mobile = models.CharField(max_length=11, verbose_name=_('Phone Number'))
    message = models.TextField(verbose_name=_('Message'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta :
        verbose_name = _('Contact message')
        verbose_name_plural = _('Contact messages')
        ordering = ('created',)


    def save(self, *args, **kwargs):
        if not phone_number.validate(self.mobile) :
            raise ValidationError(_('Phone number is not valid'))
        super(Contact, self).save(*args, **kwargs)