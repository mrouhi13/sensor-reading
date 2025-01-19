from django.urls import include, path

app_name = 'v1'

urlpatterns = [
    path('', include('apps.sensors.api.v1.urls')),
]
