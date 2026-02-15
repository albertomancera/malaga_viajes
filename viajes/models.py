from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Viaje(models.Model):
    destino = models.CharField(max_length=100)
    fecha_partido = models.DateTimeField()
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    plazas_totales = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.destino} ({self.fecha_partido.strftime('%d/%m/%Y')})"

class Inscripcion(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='inscripciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=200)
    dni = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)

class Resena(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(verbose_name="Tu opinión")
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Estrellas (1-5)"
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Opinión de {self.usuario.username}"