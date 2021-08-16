from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings

from BANPars.redis_conf import redis as r

class Command(BaseCommand):
    help = '2 options : clear the cache data (part=cache or no-input) | clear whole redis db (part=db)'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--part', type=str, help='Define an option for clearing redis db', )

    def handle(self, *args, **kwargs):
        p = kwargs['part']

        if p == 'db':
            cache.clear()
            self.stdout.write('Cleared redis db\n')

        elif p == 'cache' or p == None :
            prefix=settings.CACHES['default']['KEY_PREFIX']
            for key in r.scan_iter(f'{prefix}*'):
                r.delete(key)
            self.stdout.write('Cleared cache\n')




