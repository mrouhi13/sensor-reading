from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.sensors.api.v1.views import SensorReadingViewSet

app_name = 'sensors'

router = DefaultRouter()
router.register(r'sensor-reading', SensorReadingViewSet)

urlpatterns = [
    path('', include((router.urls, app_name))),
]
