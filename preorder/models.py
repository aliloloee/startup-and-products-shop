from django.db import models
from django.utils.translation import gettext_lazy as _

from store.models import Product
from customUser.models import validate_number, User


class PreOrder(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name=_('Product'), null=True)
    fullname = models.CharField(max_length=255, verbose_name=_('Fullname'))
    phone_number = models.CharField(max_length=11, validators=[validate_number],
                                    verbose_name=_('Phone number'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta :
        verbose_name = _('Pre-Order')
        verbose_name_plural = _('Pre-Orders')
        ordering            = ('-created',)

    def __str__(self):
        return f'Pre-Order set by {self.user}'

