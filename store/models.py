from customUser.models import User
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from . models_utils import LowerCharField, image_directory_path, transparent_image_directory_path
from BANPars.cache_updater import updater



class Category (models.Model) :
    name = LowerCharField(max_length=150, verbose_name=_('Category Name'))


    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name=_('Slug'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Product (models.Model) :

    class ProductManager(models.Manager) :
        def get_queryset(self) :
            return super().get_queryset().filter(is_active=True)

    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, verbose_name=_('Category'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    transparent_image = models.ImageField(verbose_name=_("Transparent Image"),
                                help_text=_("Upload a Transparent image."),
                                upload_to=transparent_image_directory_path,
                                default="images/default.png")

    price = models.DecimalField(max_digits=8, decimal_places=0, verbose_name=_('Price'),
                                help_text=_('Maximum 99 milion toman'),
                                error_messages={
                                    "name" : {
                                        "max_length": _('The price must be between 0 and 99.999.999 toman'),
                                    }
                                })

    discount_price = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True,
                                verbose_name=_("Discount Price"),
                                help_text=_("Maximum 99 milion toman"),
                                error_messages={
                                    "name": {
                                        "max_length": _("The price must be between 0 and 999.99."),
                                    },
                                })

    # in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name=_('Slug'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        updater.clear_model_template_cache(model_name=Product.__name__)
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductImage(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="product_image", verbose_name=_('Product'))
    image = models.ImageField(verbose_name=_("Image"), help_text=_("Upload a product image"),
                                upload_to=image_directory_path, default="images/default.png")

    alt_text = models.CharField(verbose_name=_("Alternative text"), help_text=_("Please add alternative text"),
                                max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        updater.clear_model_template_cache(model_name=ProductImage.__name__, foreignkey_id=self.product.id)
        super(ProductImage, self).save(*args, **kwargs)

    def __str__(self) :
        return f'Image of product_id = {self.product.pk}'


class Feature (models.Model) :

    class ActiveObjects(models.Manager) :
        def get_queryset(self) :
            return super().get_queryset().filter(is_active=True)

    product = models.ManyToManyField(Product, related_name='features', verbose_name=_('Product'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    price = models.DecimalField(max_digits=7, decimal_places=0, verbose_name=_('Price'),
                                help_text=_('Maximum 9 milion toman'),
                                error_messages={
                                    "name" : {
                                        "max_length": _('The price must be between 0 and 9.999.999 toman'),
                                    }
                                })
    

    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    actives = ActiveObjects()
    objects = models.Manager()

    class Meta:
        verbose_name = _('Feature')
        verbose_name_plural = _('Features')
        ordering = ('-created',)

    def __str__(self):
        return f'Feature : {self.name}'


class OptionCategory (models.Model) :
    product = models.ManyToManyField(Product, related_name='titles', verbose_name=_('Product'))
    name = LowerCharField(max_length=150, verbose_name=_('Title Name'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _('Option title')
        verbose_name_plural = _('Option titles')
        ordering = ('-created',)

    def __str__(self):
        return self.name


class Option (models.Model) :

    class ActiveObjects(models.Manager) :
        def get_queryset(self) :
            return super().get_queryset().filter(is_active=True)

    title = models.ForeignKey(OptionCategory, on_delete=models.CASCADE, related_name='options', verbose_name=_('Title'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    price = models.DecimalField(max_digits=7, decimal_places=0, verbose_name=_('Price'),
                                help_text=_('Maximum 9 milion toman'),
                                error_messages={
                                    "name" : {
                                        "max_length": _('The price must be between 0 and 9.999.999 toman'),
                                    }
                                })

    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    actives = ActiveObjects()
    objects = models.Manager()

    class Meta:
        verbose_name = _('Option')
        verbose_name_plural = _('Options')
        ordering = ('-created',)

    def __str__(self):
        return f'Option : {self.name}, for category of {self.title.name}'


