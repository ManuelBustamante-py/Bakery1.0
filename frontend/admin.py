# admin.py
from django.contrib import admin
from .models import Producto, MensajeContacto

admin.site.register(Producto)

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'asunto', 'fecha_envio']
    search_fields = ['nombre', 'email', 'asunto']
    list_filter = ['fecha_envio']
