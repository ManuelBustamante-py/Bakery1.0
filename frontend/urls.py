# frontend/urls.py
from .views import check_auth
from django.urls import path
from . import views
from .views import obtener_stock
from .views import procesar_pago, enviar_resumen
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'), 
    path('inicio/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('admin/', views.admin_page, name='admin_page'),
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
    path('contact/', views.contact, name='contact'),
    path('perfil/', views.perfil, name='perfil'),
    path('login/', views.login_view, name='login'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/check_auth/', check_auth, name='check_auth'),
    path('api/procesar_pago/', procesar_pago, name='procesar_pago'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('historial_compras/', views.historial_compras, name='historial_compras'),

]  

