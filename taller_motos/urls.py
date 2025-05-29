from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

# Vista de bienvenida
def home(request):
    return HttpResponse("<h1>Bienvenido al Taller de Motos</h1>")

# Swagger: habilitar soporte para JWT
class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.security_definitions = {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'JWT Authorization header using the Bearer scheme. Ej: "Bearer <tu_token>"',
            }
        }
        schema.security = [{'Bearer': []}]
        return schema

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Taller Motos",
        default_version='v1',
        description="Documentación de la API del taller de motos",
        contact=openapi.Contact(email="contacto@taller.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
schema_view.generator_class = BothHttpAndHttpsSchemaGenerator

# URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # Rutas apps
    path('api/', include('citas.urls')),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger y Redoc
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
