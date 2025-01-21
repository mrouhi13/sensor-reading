from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.sensors.api.v1.views import SensorReadingViewSet, SensorViewSet

app_name = 'sensors'

router = DefaultRouter()
router.register(r'sensors', SensorViewSet)
router.register(r'readings', SensorReadingViewSet)

urlpatterns = [
    path('', include((router.urls, app_name))),
]
