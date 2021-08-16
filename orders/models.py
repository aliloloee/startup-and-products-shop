from django.db import models
from django.utils.translation import gettext_lazy as _

from customUser.models import User
from store.models import Product, Feature, Option
from addresses.models import Province, City



class Order (models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE,
                    related_name='orders', verbose_name=_('User'))
    fullname     = models.CharField(max_length=50, verbose_name=_('Fullname'))
    address      = models.TextField(max_length=500, verbose_name=_('Address'))
    delivery_instructions  = models.TextField(max_length=500,
                            verbose_name=_('Delivery instructions'), blank=True, default='')

    province = models.ForeignKey(Province, on_delete=models.PROTECT, verbose_name=_('Province'))
    city         = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name=_('City'))

    phone        = models.CharField(max_length=11, verbose_name=_('Phone Number'))
    post_code    = models.CharField(max_length=20, verbose_name=_('Post Code'))
    paid         = models.BooleanField(default=False, verbose_name=_('Is Paid'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name        = _('Order')
        verbose_name_plural = _('Orders')
        ordering            = ('-created',)

    def get_total_cost(self) :
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        return f'Order by {self.user} at {self.created}'

class OrderProductItem (models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name=_('Product'))
    price      = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    quantity   = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))

    class Meta:
        verbose_name        = _('Order Product')
        verbose_name_plural = _('Order Products')

    def get_cost(self) :
        return self.price * self.quantity

    def __str__(self) :
        return str(self.id)


class OrderFeatureItem (models.Model):
    order_product   = models.ForeignKey(OrderProductItem,
                            on_delete=models.CASCADE,
                            related_name='feature_items',
                            verbose_name=_('Product'))

    feature         = models.ForeignKey(Feature,
                            on_delete=models.CASCADE,
                            related_name='order_features',
                            verbose_name=_('Related Feature'))

    price           = models.DecimalField(max_digits=4,
                            decimal_places=2,
                            verbose_name=_('Feature Price'))

    class Meta:
        verbose_name        = _('Feature Related To Ordering Product')
        verbose_name_plural = _('Features Related To Ordering Products')

    def __str__(self) :
        return str(self.id)

class OrderOptionItem (models.Model):
    order_product = models.ForeignKey(OrderProductItem,
                            on_delete=models.CASCADE,
                            related_name='option_items',
                            verbose_name=_('Product'))

    option        = models.ForeignKey(Option,
                            on_delete=models.CASCADE,
                            related_name='order_options',
                            verbose_name=_('Related Option'))

    price         = models.DecimalField(max_digits=4,
                            decimal_places=2,
                            verbose_name=_('Option Price'))

    class Meta:
        verbose_name        = _('Option Related To Ordering Product')
        verbose_name_plural = _('Options Related To Ordering Products')

    def __str__(self) :
        return str(self.id)