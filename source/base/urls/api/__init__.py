from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('v1/', include('base.urls.api.v1')),
]
