from modeltranslation.translator import register, TranslationOptions
from . models import Category, Product, ProductImage, OptionCategory, Option, Feature


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(ProductImage)
class ProductImageTranslationOptions(TranslationOptions):
    fields = ('alt_text', )

@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(OptionCategory)
class OptionCategoryTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(Option)
class OptionTranslationOptions(TranslationOptions):
    fields = ('name', )
