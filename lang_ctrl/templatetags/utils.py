from django.conf import settings
from django.utils.translation import gettext_lazy as _

def switch_lang_code(path, language):
    lang_codes = [c for (c, name) in settings.LANGUAGES]

    if path == '':
        raise Exception(_('URL path for language switch is empty'))
    elif path[0] != '/':
        raise Exception(_('URL path for language switch does not start with "/"'))
    elif language not in lang_codes:
        raise Exception(_('Language code not supported.'))

    parts = path.split('/')
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language
    return '/'.join(parts)