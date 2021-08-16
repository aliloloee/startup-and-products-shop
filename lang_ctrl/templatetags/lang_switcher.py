from django import template
from django.template.defaultfilters import stringfilter

from .utils import switch_lang_code

register = template.Library()

@register.filter
@stringfilter
def switch_lang_prefix(path, language):
    return switch_lang_code(path, language)

@register.filter
def switch_lang(request, language):
    return switch_lang_code(request.get_full_path(), language)