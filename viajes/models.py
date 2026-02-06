from django.db import models
from django.contrib.auth.models import User

class Viaje(models.Model):
    destino = models.CharField(max_length=100)
    fecha_partido = models.DateTimeField()
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    plazas_totales = models.PositiveIntegerField()

    def __str__(self):
        return f"Viaje a {self.destino}"

class Inscripcion(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='inscripciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=200)
    dni = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)