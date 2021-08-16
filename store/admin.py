from customUser.models import User
from django.contrib import admin

from .models import Category, Product, Feature, OptionCategory, Option, ProductImage


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin) :
    list_display = ('pk', 'get_product')
    list_filter = (
        ('product__id', custom_titled_filter('PRODUCT ID')),
    )

    @admin.display(description='Product ID')
    def get_product(self, obj) :
        return f'{obj.product.pk}'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(OptionCategory)
class OptionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    list_filter = ['product__title', ]

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'title']
    list_filter = ['title__product', ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price']
    list_filter = ['is_active', ]
    list_editable = ['price',]
    prepopulated_fields = {'slug': ('title',)}

    # # In order to only have the staff users able to add product
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     form.base_fields['created_by'].queryset = User.objects.filter(is_staff=True)
    #     return form

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin) :
    list_display = ['name', 'price', 'is_active', ]
    list_filter = ['is_active', ]
    list_editable = ['price',]