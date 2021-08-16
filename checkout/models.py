from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryOptions(models.Model):

    DELIVERY_CHOICES = [
        ("IS", _("In Store")),
        ("HD", _("Home Delivery")),
        ("DD", _("Digital Delivery")),
    ]

    delivery_name = models.CharField(
        verbose_name=_("Delivery_name"),
        max_length=255,
    )
    delivery_price = models.DecimalField(
        verbose_name=_("Delivery price"),
        help_text=_("Maximum 999,999.00"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999,999.00"),
            },
        },
        max_digits=6,
        decimal_places=0,
    )
    delivery_method = models.CharField(
        choices=DELIVERY_CHOICES,
        verbose_name=_("Delivery method"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_timeframe = models.CharField(
        verbose_name=_("Delivery timeframe"),
        max_length=255,
    )
    delivery_window = models.CharField(
        verbose_name=_("Delivery window"),
        max_length=255,
    )
    order = models.IntegerField(verbose_name=_("list order"), help_text=_("Required"), default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    def __str__(self):
        return self.delivery_name

class PaymentSelection(models.Model):

    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Payment Selection")
        verbose_name_plural = _("Payment Selections")

    def __str__(self):
        return self.name