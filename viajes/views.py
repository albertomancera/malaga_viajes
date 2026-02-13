from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
import openpyxl
from .models import Viaje, Inscripcion

# ==============================================================================
# SECCIÓN 1: PÁGINAS PÚBLICAS
# ==============================================================================

def inicio(request):
    hoy = timezone.now()
    viajes_lista = Viaje.objects.filter(fecha_partido__gte=hoy).order_by('fecha_partido')[:3]
    
    for v in viajes_lista:
        v.plazas_libres = v.plazas_totales - v.inscripciones.count()
        # Calculamos el porcentaje para la barra (opcional)
        v.porcentaje_llenado = (v.inscripciones.count() / v.plazas_totales) * 100

    return render(request, 'viajes/inicio.html', {'viajes': viajes_lista})

# ==============================================================================
# SECCIÓN 2: GESTIÓN DE CUENTAS (Registro)
# ==============================================================================

def registro(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'cuentas/registro.html', {'form': form})


# ==============================================================================
# SECCIÓN 3: GESTIÓN DE RESERVAS (Requiere Login)
# ==============================================================================

@login_required
def inscribirse(request, viaje_id):

    viaje = get_object_or_404(Viaje, id=viaje_id)

   
    plazas_ocupadas = viaje.inscripciones.count()
    plazas_libres = viaje.plazas_totales - plazas_ocupadas

    if request.method == 'POST':
        
        
        if viaje.inscripciones.count() < viaje.plazas_totales:
            Inscripcion.objects.create(
                viaje=viaje,
                usuario=request.user, 
                nombre_completo=request.POST.get('nombre'),
                dni=request.POST.get('dni'),
                telefono=request.POST.get('telefono')
            )
            return render(request, 'viajes/exito.html', {'viaje': viaje})
        else:
            
            return render(request, 'viajes/formulario_inscripcion.html', {
                'viaje': viaje,
                'error': '¡Lo sentimos, el bus se acaba de llenar!',
                'plazas_libres': 0
            })

    
    return render(request, 'viajes/formulario_inscripcion.html', {
        'viaje': viaje,
        'plazas_libres': plazas_libres
    })


@login_required
def mis_reservas(request):
    """
    Muestra solo las reservas del usuario que ha iniciado sesión.
    """
    reservas = Inscripcion.objects.filter(usuario=request.user).order_by('-fecha_registro')
    return render(request, 'viajes/mis_reservas.html', {'reservas': reservas})

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Inscripcion, id=reserva_id, usuario=request.user)

 
    nombre_destino = reserva.viaje.destino

    reserva.delete()

    return render(request, 'viajes/reserva_cancelada.html', {'destino_nombre': nombre_destino})


# ==============================================================================
# SECCIÓN 4: HERRAMIENTAS DE ADMINISTRACIÓN (Solo Staff)
# ==============================================================================

@login_required
def exportar_pasajeros_excel(request, viaje_id):
    """
    Genera y descarga un Excel con la lista de pasajeros.
    Solo accesible para usuarios Staff (Admin).
    """
    if not request.user.is_staff:
        return redirect('inicio')

    viaje = get_object_or_404(Viaje, id=viaje_id)
    inscritos = viaje.inscripciones.all()

    wb = openpyxl.Workbook()
    hoja = wb.active
    hoja.title = f"Pasajeros {viaje.destino}"

    
    hoja.append(['Nombre Completo', 'DNI', 'Teléfono', 'Fecha Registro'])

    
    for inscripcion in inscritos:
        
        fecha_fmt = inscripcion.fecha_registro.strftime('%d/%m/%Y %H:%M')
        hoja.append([
            inscripcion.nombre_completo, 
            inscripcion.dni, 
            inscripcion.telefono, 
            fecha_fmt
        ])

   
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Listado_{viaje.destino}.xlsx"'
    wb.save(response)

    return response

