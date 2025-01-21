from unittest.mock import MagicMock, patch

from django.test import TestCase
from requests.exceptions import Timeout

from services import API_BASE_URL, fetch_sensor_data
from services.tasks import fetch_sensor_data_task


class FetchSensorDataTestCase(TestCase):

    @patch('requests.get')
    def test_successful_api_call(self, mock_requests_get):
        # Simulate a successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'sensor_id': 1, 'timestamp': '2025-01-01T12:00:00Z',
             'value': 25.3},
            {'sensor_id': 2, 'timestamp': '2025-01-01T12:05:00Z',
             'value': 30.7},
        ]
        mock_requests_get.return_value = mock_response

        result = fetch_sensor_data()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['sensor_id'], 1)

    @patch('requests.get')
    def test_failed_api_call(self, mock_requests_get):
        # Simulate a failed API response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {}
        mock_requests_get.return_value = mock_response

        result = fetch_sensor_data()

        self.assertEqual(result, {})

    @patch('requests.get', side_effect=Timeout)
    def test_api_timeout(self, mock_requests_get):
        result = fetch_sensor_data()

        mock_requests_get.assert_called_once()

        self.assertEqual(result, {})



class TestFetchSensorDataTask(TestCase):

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

        fetch_sensor_data_task()

        # Verify that the requests.get was called with the correct URL
        mock_get.assert_called_once_with(API_BASE_URL)

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

        fetch_sensor_data_task()
        mock_get.assert_called_once_with(API_BASE_URL)
