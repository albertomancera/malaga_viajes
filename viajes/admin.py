from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Viaje, Inscripcion

@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('destino', 'fecha_partido', 'precio', 'get_ocupacion', 'descargar_excel')
    list_filter = ('destino', 'fecha_partido')
    
    def get_ocupacion(self, obj):
        # Muestra una barra de progreso visual en el admin
        total = obj.plazas_totales
        ocupadas = obj.inscripciones.count()
        porcentaje = (ocupadas / total) * 100
        color = "#28a745" if porcentaje < 80 else "#dc3545"
        return format_html(
            '<b style="color: {};">{} / {}</b>',
            color, ocupadas, total
        )
    get_ocupacion.short_description = "Ocupación"

    def descargar_excel(self, obj):
        # Botón para bajar el Excel de pasajeros
        url = reverse('exportar_excel', args=[obj.id])
        return format_html('<a class="button" href="{}" style="background:#6CABDD; color:white;">📥 Bajar Lista</a>', url)
    descargar_excel.short_description = "Acciones"

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'dni', 'viaje', 'fecha_registro')
    search_fields = ('nombre_completo', 'dni')
    list_filter = ('viaje',)