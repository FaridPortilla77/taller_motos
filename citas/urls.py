from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CitaViewSet,
    ClienteViewSet,
    MotoViewSet,
    ServicioViewSet,
    mis_citas,
    RegisterUserView,
    UserListView,
    LoginView,
    AgendarCitaLibreView  # 👈 NUEVA VISTA IMPORTADA
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'citas', CitaViewSet)
router.register(r'motos', MotoViewSet)
router.register(r'servicios', ServicioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registro/', RegisterUserView.as_view(), name='registro-usuario'),
    path('users/', UserListView.as_view(), name='lista-usuarios'),
    path('login/', LoginView.as_view(), name='login'),
    path('mis-citas/', mis_citas, name='mis-citas'),
    path('agendar-cita-libre/', AgendarCitaLibreView.as_view(), name='agendar-cita-libre'),  # 👈 NUEVA RUTA
]
