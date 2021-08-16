from django.conf import settings

def cache_time(request) :
    return {
        'cache_ttl' : settings.CACHE_TTL,
    }