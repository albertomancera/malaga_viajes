from django.contrib import admin
from django.urls import path, include
from viajes import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('inscribirse/<int:viaje_id>/', views.inscribirse, name='inscribirse'),
    
    # Sistema de login/logout
    path('cuentas/', include('django.contrib.auth.urls')),
]