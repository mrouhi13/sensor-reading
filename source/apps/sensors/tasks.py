import requests
from django.conf import settings
from rest_framework import status

from apps.sensors.models import SensorReading
from base import celery_app


@celery_app.task
def fetch_sensor_data() -> None:
    """
    A celery task to fetch and store sensor data from an external API
    """
    response = requests.get(settings.EXTERNAL_API_URL)

    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        SensorReading.objects.bulk_create([
            SensorReading(
                sensor_id=item['sensor_id'],
                timestamp=item['timestamp'],
                value=item['value']
            ) for item in data
        ])
