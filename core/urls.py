from django.contrib import admin
from django.urls import path, include
from viajes import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('inscribirse/<int:viaje_id>/', views.inscribirse, name='inscribirse'),
    path('mis_reservas/', views.mis_reservas, name='mis_reservas'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('exportar-excel/<int:viaje_id>/', views.exportar_pasajeros_excel, name='exportar_excel'),
    path('agregar_resena/', views.agregar_resena, name='agregar_resena'),
    
    # Sistema de login/logout
    path('cuentas/', include('django.contrib.auth.urls')),
]