from django.shortcuts import render, redirect

from .models import Viaje, Inscripcion

# Create your views here.
def inicio(request):
    proximos_viajes = Viaje.objects.all().order_by('fecha_partido')
    
    return render(request, 'viajes/inicio.html', {'viajes': proximos_viajes})

def inscribirse(request, viaje_id):
    try:
        viaje = Viaje.objects.get(id = viaje_id)
    except Viaje.DoesNotExist:
        return redirect('inicio')
    
    error = None
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        dni = request.POST.get('dni').upper()
        telefono = request.POST.get('telefono')

        if len(dni) != 9:
            error = "El DNI debe tener 8 números y 1 letra."
        
        elif viaje.inscripciones.count() >= viaje.plazas_totales:
            error = "Lo sentimos, ¡el bus ya está lleno!"

        if not error:
            Inscripcion.objects.create(
                viaje=viaje,
                nombre_completo=nombre,
                dni=dni,
                telefono=telefono
            )
            return render(request, 'viajes/exito.html', {'viaje': viaje})

    return render(request, 'viajes/formulario_inscripcion.html', {
        'viaje': viaje,
        'error': error,
        'plazas_libres': viaje.plazas_totales - viaje.inscripciones.count()
    })