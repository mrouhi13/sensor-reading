from django.conf import settings
from django.http import HttpResponseBase
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

from apps.sensors.api.v1.serializers import SensorReadingSerializer


class SensorReadingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sensor readings to be viewed or edited.
    """
    serializer_class = SensorReadingSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = {
        'sensor_id': ['exact'],
        'timestamp': ['gte', 'lte', 'exact', 'gt', 'lt'],
    }

    @method_decorator(cache_page(settings.CACHE_TTL))
    def dispatch(self, request, *args, **kwargs) -> HttpResponseBase:
        """
        Dispatch method for the view set that caches the response.
        """
        return super().dispatch(request, *args, **kwargs)
