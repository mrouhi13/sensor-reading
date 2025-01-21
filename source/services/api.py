import requests
from rest_framework import status

API_BASE_URL = 'https://external-api.com/sensors'


def fetch_sensor_data() -> dict:
    """
    Fetch sensor data from an external API.
    :return:
    """
    data = {}
    try:
        response = requests.get(API_BASE_URL)

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
    except requests.exceptions.Timeout:
        # Send log to error tracking service (e.g. Sentry)
        pass

    return data
