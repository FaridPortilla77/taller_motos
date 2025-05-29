from rest_framework import serializers
from .models import Cliente, Moto, Servicio, Cita

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class MotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moto
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'descripcion', 'precio']  


class CitaSerializer(serializers.ModelSerializer):
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    moto_modelo = serializers.CharField(source='moto.modelo', read_only=True)

    class Meta:
        model = Cita
        fields = ['id', 'servicio', 'servicio_nombre', 'moto', 'moto_modelo', 'fecha', 'hora', 'estado', 'informe']



from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']