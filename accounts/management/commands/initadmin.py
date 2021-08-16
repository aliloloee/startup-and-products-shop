from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from decouple import config


class Command(BaseCommand):
    help = 'Create superuser from env file credentials'

    def handle(self, *args, **options):
        if get_user_model().objects.count() == 0:

            username = config('DJANGO_SUPERUSER_USERNAME')
            password = config('DJANGO_SUPERUSER_PASSWORD')

            admin = get_user_model().objects.create_superuser(username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else :
            self.stdout.write('Auth-User table not empty \n')