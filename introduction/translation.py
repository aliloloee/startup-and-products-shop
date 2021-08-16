from modeltranslation.translator import register, TranslationOptions
from . models import Service, Benefit, TeamMember, Banner


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(Benefit)
class BenefitTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(TeamMember)
class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('introduction', 'fullname', 'role', )

@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)
