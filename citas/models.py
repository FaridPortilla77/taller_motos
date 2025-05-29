from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario   = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono  = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)

    def __str__(self):
        return self.usuario.username


class Moto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.cliente.usuario.username}"

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Cita(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    hora = models.TimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('completado', 'Completado'),
            ('cancelada', 'Cancelada')
        ],
        default='pendiente'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    informe = models.TextField(blank=True, null=True)  
    def __str__(self):
        return f"Cita {self.id} - {self.cliente.usuario.username} - {self.servicio.nombre}"

