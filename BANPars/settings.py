from pathlib import Path
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from datetime import timedelta
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'


SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Internal Apps
    'django.contrib.humanize',

    # Local Apps
    'customUser',
    'accounts.apps.AccountsConfig',
    'introduction',
    'store',
    'basket',
    'lang_ctrl',
    'addresses',
    'checkout',
    'orders',
    'preorder',
    # 'bucket',

    # Third-Party Apps
    'widget_tweaks',
    'modeltranslation',
    'django_celery_beat',
    # 'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BANPars.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Categories
                'store.context_processors.categories',
                # Cart
                'basket.context_processors.basket',
                # Avatar
                'accounts.context_processors.avatar',
                # Cache_ttl
                'BANPars.context_processors.cache_time',
            ],
        },
    },
]



AUTH_USER_MODEL = 'customUser.User'

WSGI_APPLICATION = 'BANPars.wsgi.application'




# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'startup',
#         'USER': 'postgres', 
#         'PASSWORD': 'ali90055',
#         'HOST': '127.0.0.1', 
#         'PORT': '5432',
#     }
# }

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         },
#         "KEY_PREFIX": "caching"
#     }
# }



# Dockerized databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_DB'), 
        'USER': config('POSTGRES_USER'), 
        'PASSWORD': config('POSTGRES_PASSWORD'), 
        'HOST': 'postgresql_db', 
        'PORT': '5432',
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://cache:6379/1",
        "OPTIONS": {
            "PASSWORD" : config('REDIS_PASS'),
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "caching"
    }
}


CACHE_DB_NUMBER = 1


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


MESSAGE_TAGS = {
    messages.ERROR : 'error',
    messages.SUCCESS : 'success',
}


# Local for Translation
LOCALE_PATHS = (
    BASE_DIR / 'locale',
)

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGES = (
    ('en', _('English')),
    ('fa', _('Persian')),
    ('ar', _('Arabic')),
)

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Kavenegar API Key
KAVENEGAR_API_KEY = config('KAVENEGAR_API_KEY')
OTP_LENGTH = 4
OTP_EXPIRATION_TIMESTAMP = 60

## (timestamp) seconds after sending the activation link, It will be expired
PASSWORD_RESET_TIMEOUT = 100


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR, ]

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


# Profile picture limitations
PROFILE_MAX_SIZE = 1*1024*1024
PROFILE_WIDTH = 700
PROFILE_HEIGHT = PROFILE_WIDTH


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Celery configs
redis_pass = config('REDIS_PASS')
CELERY_BROKER_URL = f'redis://:{redis_pass}@redis_db:6379/0'
CELERY_RESULT_BACKEND = f'redis://:{redis_pass}@redis_db:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json', ]
CELERY_RESULT_EXPIRES = timedelta(days=1)
CELERY_TASK_ALWAYS_EAGER = False
CELERY_WORKER_PREFETCH_MULTIPLIER = 4


# Celerybeat thereshold times
NOT_ACTIVATED_USERS_THERESHOLD = 24

# Cache TTL
CACHE_TTL = 7*24*60*60

# auth urls
LOGIN_REDIRECT_URL = "introduction:company"
LOGOUT_REDIRECT_URL = "introduction:company"
LOGIN_URL = "accounts:login"
LOGOUT_URL = 'accounts:logout'

