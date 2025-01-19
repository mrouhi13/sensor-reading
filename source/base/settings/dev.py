"""Development settings."""
from base.settings.base import * # noqa

AUTH_PASSWORD_VALIDATORS = []

CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
}

CORS_ALLOW_ALL_ORIGINS = True

CACHE_TTL = 0  # seconds
