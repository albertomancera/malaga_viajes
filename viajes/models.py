from django.db import models

# Create your models here.
class Viaje(models.Model):
    destino = models.CharField(max_length=100)
    fecha_partido = models.DateTimeField()
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    plazas_totales = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='fotos_viajes/', null=True, blank=True)

    def __str__(self):
        return f"Viaje a {self.destino} - {self.fecha_partido.strftime('%d/%m/%Y')}"