from django.shortcuts import render
from .models import Viaje

# Create your views here.
def home(request):
    proximos_viajes = Viaje.objects.all().order_by('fecha_partido')
    
    return render(request, 'inicio.html', {'viajes': proximos_viajes})