from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.sensors.models import Sensor, SensorReading


class SensorReadingTests(APITestCase):
    def setUp(self):
        """
        Set up test data for the API endpoints.
        """
        self.sensor = Sensor.objects.create(name='Test Sensor',
                                            location='Test Location')
        self.reading_1 = SensorReading.objects.create(
            sensor=self.sensor,
            timestamp=datetime.now() - timedelta(hours=1),
            value=10.5
        )
        self.reading_2 = SensorReading.objects.create(
            sensor=self.sensor,
            timestamp=datetime.now() - timedelta(hours=2),
            value=20.5
        )
        self.reading_3 = SensorReading.objects.create(
            sensor=self.sensor,
            timestamp=datetime.now() - timedelta(hours=3),
            value=30.5
        )

        self.base_url = reverse('api:v1:sensors:sensors:sensorreading-list')

    def test_list_sensor_readings(self):
        """
        Test the list sensor readings endpoint.
        """
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['sensor'], self.sensor.id)
        self.assertEqual(response.data[0]['value'], self.reading_1.value)

    def test_filter_sensor_readings_by_sensor_id(self):
        """
        Test filtering sensor readings by sensor_id.
        """
        response = self.client.get(self.base_url, {'sensor_id': self.sensor.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['sensor'], self.sensor.id)

    def test_create_sensor_reading(self):
        """
        Test creating a new sensor reading.
        """
        timestamp = datetime.now().isoformat()
        data = {
            'sensor': self.sensor.id,
            'timestamp': timestamp,
            'value': 15.5
        }
        response = self.client.post(self.base_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sensor'], self.sensor.id)
        self.assertEqual(response.data['value'], 15.5)

    def test_create_sensor_reading_invalid_data(self):
        """
        Test creating a sensor reading with invalid data.
        """
        data = {
            'sensor': self.sensor.id,
            'timestamp': 'invalid-timestamp',
            'value': 'invalid-value'
        }
        response = self.client.post(self.base_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
