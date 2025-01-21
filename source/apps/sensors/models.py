from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class Sensor(models.Model):
    id = models.UUIDField(
        verbose_name=_('ID'),
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
        unique=True,
    )
    location = models.CharField(
        verbose_name=_('Location'),
        max_length=255,
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('Sensor')
        verbose_name_plural = _('Sensors')

    def __str__(self) -> str:
        return self.name


class SensorReading(models.Model):
    id = models.UUIDField(
        verbose_name=_('ID'),
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    sensor = models.ForeignKey(
        verbose_name=_('Sensor ID'),
        to='Sensor',
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(
        verbose_name=_('Timestamp'),
        db_index=True,
    )
    value = models.FloatField(
        verbose_name=_('Value'),
    )

    class Meta:
        verbose_name = _('Sensor Reading')
        verbose_name_plural = _('Sensor Readings')
        indexes = [
            models.Index(fields=['sensor_id', 'timestamp']),
        ]

    def __str__(self) -> str:
        return f'Sensor {self.sensor} at {self.timestamp}: {self.value}'
