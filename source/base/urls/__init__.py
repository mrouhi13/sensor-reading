"""URL configuration."""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls.api')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

    urlpatterns += [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'),
             name='swagger-ui'),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
