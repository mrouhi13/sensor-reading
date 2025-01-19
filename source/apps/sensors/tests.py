import unittest
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import TestCase

from apps.sensors.models import Sensor, SensorReading
from apps.sensors.tasks import fetch_sensor_data


class SensorModelTestCase(TestCase):

    def test_sensor_creation(self):
        sensor = Sensor.objects.create(name='Test Sensor', location='Lab')
        self.assertEqual(sensor.name, 'Test Sensor')

        # Test __str__ method
        self.assertEqual(sensor.__str__(), sensor.name)


class SensorReadingModelTestCase(TestCase):

    def test_sensor_reading_creation(self):
        sensor_reading = SensorReading.objects.create(
            sensor=Sensor.objects.create(
                name='Sensor 1',
                location='Location 1',
            ),
            timestamp='2022-01-01 00:00:00',
            value=1.0,
        )
        self.assertEqual(sensor_reading.value, 1.0)

        # Test __str__ method
        self.assertEqual(sensor_reading.__str__(),
                         f'Sensor {sensor_reading.sensor} at '
                         f'{sensor_reading.timestamp}: {sensor_reading.value}')


class TestFetchSensorDataFromAPI(unittest.TestCase):

    @patch('requests.get')
    @patch('apps.sensors.models.SensorReading.objects.bulk_create')
    def test_fetch_sensor_data_success(self, mock_bulk_create, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'sensor_id': 1, 'timestamp': '2025-01-01T12:00:00Z',
             'value': 25.3},
            {'sensor_id': 2, 'timestamp': '2025-01-01T12:05:00Z',
             'value': 30.7},
        ]
        mock_get.return_value = mock_response

        fetch_sensor_data()

        # Verify that the requests.get was called with the correct URL
        mock_get.assert_called_once_with(settings.EXTERNAL_API_URL)

        # Verify that bulk_create was called with the expected objects
        mock_bulk_create.assert_called_once()
        created_objects = mock_bulk_create.call_args[0][0]
        self.assertEqual(len(created_objects), 2)
        self.assertEqual(created_objects[0].sensor_id, 1)
        self.assertEqual(created_objects[0].timestamp, '2025-01-01T12:00:00Z')
        self.assertEqual(created_objects[0].value, 25.3)

    @patch('requests.get')
    def test_fetch_sensor_data_api_failure(self, mock_get):
        # Mock a failed API response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        fetch_sensor_data()
        mock_get.assert_called_once_with(settings.EXTERNAL_API_URL)
