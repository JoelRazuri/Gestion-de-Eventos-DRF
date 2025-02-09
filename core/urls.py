from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('events.urls')),
    path('api/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # Genera el esquema OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Documentación interactiva (Swagger UI)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

urlpatterns = format_suffix_patterns(urlpatterns)