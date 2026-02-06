from django.contrib import admin
from .models import Viaje, Inscripcion

@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    # Esto muestra columnas en la lista de viajes
    list_display = ('destino', 'fecha_partido', 'precio', 'plazas_totales', 'get_inscritos')
    
    # Función para mostrar cuántos van ya apuntados
    def get_inscritos(self, obj):
        return f"{obj.inscripciones.count()} / {obj.plazas_totales}"
    
    get_inscritos.short_description = 'Ocupación (Inscritos / Totales)'

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    # Columnas para ver los datos del aficionado
    list_display = ('nombre_completo', 'dni', 'viaje', 'fecha_registro')
    
    # Filtro lateral para buscar por viaje rápidamente
    list_filter = ('viaje', 'fecha_registro')
    
    # Buscador por nombre o DNI
    search_fields = ('nombre_completo', 'dni')