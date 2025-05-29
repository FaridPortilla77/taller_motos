from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.exceptions import PermissionDenied

from .models import Cliente, Moto, Servicio, Cita
from .serializers import (
    ClienteSerializer,
    MotoSerializer,
    ServicioSerializer,
    CitaSerializer,
    UserRegisterSerializer,
    UserSerializer
)

# ----- VIEWS PARA MODELOS CRUD -----

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class MotoViewSet(viewsets.ModelViewSet):
    queryset = Moto.objects.all()
    serializer_class = MotoSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Cita.objects.all().order_by('-fecha')
        cliente = Cliente.objects.get(usuario=self.request.user)
        return Cita.objects.filter(cliente=cliente).order_by('-fecha')

    def perform_create(self, serializer):
        cliente = Cliente.objects.get(usuario=self.request.user)
        serializer.save(cliente=cliente)

    def perform_update(self, serializer):
        cita = serializer.instance

        if self.request.user.is_staff:
            serializer.save()
            return

        try:
            cliente = Cliente.objects.get(usuario=self.request.user)
        except Cliente.DoesNotExist:
            raise PermissionDenied("No tienes un perfil de cliente.")

        if cita.cliente != cliente:
            raise PermissionDenied("No tienes permiso para editar esta cita.")

        serializer.save()

# ----- REGISTRO DE USUARIO -----

@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Cliente.objects.create(usuario=user)
            return Response({"mensaje": "Usuario y perfil Cliente creados"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----- LISTADO DE USUARIOS -----

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ----- INICIO DE SESIÓN -----

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Se requieren usuario y contraseña"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({
                "mensaje": "Login exitoso",
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff
            }, status=status.HTTP_200_OK)

        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

# ----- MIS CITAS DEL CLIENTE LOGUEADO -----

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_citas(request):
    try:
        cliente = Cliente.objects.get(usuario=request.user)
        citas = Cita.objects.filter(cliente=cliente).order_by('-fecha')
        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        return Response({"error": "Este usuario no tiene un perfil de cliente."}, status=status.HTTP_404_NOT_FOUND)

# ----- NUEVA VISTA PARA AGENDA PERSONALIZADA -----

class AgendarCitaLibreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cliente = Cliente.objects.get(usuario=request.user)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=404)

        servicio_nombre = request.data.get('servicio_nombre')
        moto_marca = request.data.get('moto_marca')
        moto_modelo = request.data.get('moto_modelo')
        moto_anio = request.data.get('moto_anio')
        fecha = request.data.get('fecha')
        hora = request.data.get('hora')

        if not all([servicio_nombre, moto_marca, moto_modelo, moto_anio, fecha]):
            return Response({"error": "Faltan campos obligatorios."}, status=400)

        servicio, _ = Servicio.objects.get_or_create(nombre=servicio_nombre, defaults={
            "descripcion": "Servicio personalizado",
            "precio": 0
        })

        moto = Moto.objects.create(cliente=cliente, marca=moto_marca, modelo=moto_modelo, anio=moto_anio)

        cita = Cita.objects.create(cliente=cliente, moto=moto, servicio=servicio, fecha=fecha, hora=hora)

        return Response({"mensaje": "Cita agendada correctamente", "cita_id": cita.id}, status=201)
