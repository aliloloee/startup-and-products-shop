from django.conf import settings
from django.core.cache.utils import make_template_fragment_key as mtfk

from . redis_conf import redis


class CacheUpdater() :
    def __init__(self, cache_db=redis) :
        self.db = cache_db
        self.db_prefix = settings.CACHES['default']['KEY_PREFIX']
        self.db_number = settings.CACHE_DB_NUMBER
        self.languages = list(item[0] for item in settings.LANGUAGES)

    def clear_model_template_cache(self, model_name, foreignkey_id=None) :
        if foreignkey_id :
            base_keys = list(mtfk(model_name.lower(), [lang, foreignkey_id, ]) for lang in self.languages)
        else :
            base_keys = list(mtfk(model_name.lower(), [lang, ]) for lang in self.languages)
        cached_banners = list(f'{self.db_prefix}:{self.db_number}:{base_key}' for base_key in base_keys)
        redis.delete(*cached_banners)


updater = CacheUpdater()