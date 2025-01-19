from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SensorsConfig(AppConfig):
    name = 'apps.sensors'
    verbose_name = _('Sensors')
