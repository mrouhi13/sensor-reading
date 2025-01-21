from apps.sensors.models import SensorReading
from base import celery_app
from services import fetch_sensor_data


@celery_app.task
def fetch_sensor_data_task() -> None:
    """
    A celery task to fetch and store sensor data from an external API
    """
    data = fetch_sensor_data()

    SensorReading.objects.bulk_create([
        SensorReading(
            sensor_id=item['sensor_id'],
            timestamp=item['timestamp'],
            value=item['value']
        ) for item in data
    ])
