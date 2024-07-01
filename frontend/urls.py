# frontend/urls.py

from django.urls import path
from . import views
from .views import obtener_stock
from .views import procesar_pago, enviar_resumen

urlpatterns = [
    path('', views.login, name='login'),
    path('inicio/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('admin/', views.admin_page, name='admin_page'),
    path('contact/', views.enviar_mensaje_contacto, name='enviar_mensaje_contacto'),  # Cambiado a 'enviar_mensaje_contacto'
    path('privacidad/', views.privacidad, name='privacidad'),
    path('product/', views.product, name='product'),
    path('service/', views.service, name='service'),
    path('team/', views.team, name='team'),
    path('terminos/', views.terminos, name='terminos'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('ventas/', views.ventas, name='ventas'),
    path('api/obtener_stock/', views.obtener_stock, name='obtener_stock'),
    path('api/procesar_pago/', views.procesar_pago, name='procesar_pago'),
    path('api/enviar_resumen/', views.enviar_resumen, name='enviar_resumen'),
    path('registro/', views.registro_usuario, name='registro'),
    path('contacto-exitoso/', views.contacto_exitoso, name='contacto_exitoso'),  # Agregada URL para éxito
]