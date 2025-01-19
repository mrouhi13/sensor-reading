"""Test settings."""
from base.settings.base import *  # noqa

AUTH_PASSWORD_VALIDATORS = []

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
}
