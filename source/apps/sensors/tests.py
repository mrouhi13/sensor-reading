from django.test import TestCase

from apps.sensors.models import Sensor, SensorReading


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
