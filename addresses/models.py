from django.db import models
from django.utils.translation import gettext_lazy as _

# import uuid
# from customUser.models import User


class Province (models.Model) :
    province = models.CharField(max_length=100, verbose_name=_('Province'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta :
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')

    def __str__(self):
        return f'{self.province}'

class City (models.Model) :
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_('Province'))
    city = models.CharField(max_length=100, verbose_name=_('City'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta :
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return f'{self.city}'


# class Address (models.Model) :
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
#     fullname = models.CharField(max_length=150, verbose_name=_('Fullname'))
#     phone = models.CharField(max_length=50, verbose_name=_('Phone number'))
#     postcode = models.CharField(max_length=15, verbose_name=_('Postcode'))
#     province = models.ForeignKey(Province, on_delete=models.PROTECT, verbose_name=_('Province'))
#     city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name=_('City'))
#     full_address = models.CharField(max_length=600, verbose_name=_('Full address'))
#     delivery_instructions = models.CharField(max_length=600, verbose_name=_('Delivery Instructions'))
#     default = models.BooleanField(default=False, verbose_name=_('Default'))

#     created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
#     updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

#     class Meta :
#         verbose_name = _('Address')
#         verbose_name_plural = _('Addresses')

#     def __str__(self):
#         return "Address"
