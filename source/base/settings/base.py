"""Base settings."""
import os
from pathlib import Path

from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DJANGO_ENV = os.getenv('DJANGO_ENV', 'dev')

REDIS_HOST = os.getenv('REDIS_HOST')

APP_CONFIG = {
    'NAME': os.getenv('APP_NAME'),
    'API_DOMAIN': os.getenv('WEB_API_DOMAIN'),
    'CONSOLE_DOMAIN': os.getenv('WEB_CONSOLE_DOMAIN'),
    'CONTACT_EMAIL': os.getenv('CONTACT_EMAIL'),
}

SECRET_KEY = 'dummy_secret_key'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', APP_CONFIG['API_DOMAIN']]

INSTALLED_APPS = [
    # Django Defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third Parties
    'rest_framework',
    'drf_spectacular',
    'django_celery_results',
    'corsheaders',
    # Local
    'apps.sensors'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=15000ms',
        },
    },
}

_PASS = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': f'{_PASS}.UserAttributeSimilarityValidator'},
    {'NAME': f'{_PASS}.MinimumLengthValidator'},
    {'NAME': f'{_PASS}.CommonPasswordValidator'},
    {'NAME': f'{_PASS}.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [f'https://{APP_CONFIG["API_DOMAIN"]}']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_HOST,
    },
}

REST_FRAMEWORK = {
    'DEFAULT_VERSION': 'v1',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

CELERY_BROKER_URL = f'{REDIS_HOST}/0'

CELERY_CACHE_BACKEND = 'django-cache'

CELERY_RESULT_BACKEND = 'django-db'

CELERY_TIMEZONE = TIME_ZONE

CELERY_RESULT_EXTENDED = True

CORS_ALLOWED_ORIGINS = []

CACHE_TTL = 300  # seconds

CELERY_BEAT_SCHEDULE = {
    'fetch_sensor_data': {
        'task': 'apps.sensors.fetch_sensor_data',
        'schedule': crontab(hour='*/1'),
    },
}
