from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='HAKATON API',
        default_version='v0.1',
        description='Документация "Гражднаский патруль"',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('docs<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
