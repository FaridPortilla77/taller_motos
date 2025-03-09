from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ServicioViewSet

router = DefaultRouter()
router.register(r'servicios', ServicioViewSet, basename='servicio')

urlpatterns = router.urls
