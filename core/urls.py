from django.contrib import admin
from django.urls import path, include
from viajes.views import inicio, inscribirse
from cuentas.views import registro 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='inicio'),
    path('inscribirse/<int:viaje_id>/', inscribirse, name='inscribirse'),
    
    # Rutas de Cuentas
    path('cuentas/', include('django.contrib.auth.urls')), 
    path('registro/', registro, name='registro'),
]