"""Import settings file based on environment."""
import os

DJANGO_ENV = os.getenv('DJANGO_ENV', 'dev')

match DJANGO_ENV:
    case 'dev':
        from base.settings.dev import *  # noq
    case 'test':
        from base.settings.test import *  # noqa
    case 'staging':
        from base.settings.staging import *  # noqa
    case 'prod':
        from base.settings.prod import *  # noqa
