# admin.py
from django.contrib import admin
from .models import Producto, MensajeContacto

admin.site.register(Producto)

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'asunto', 'mensaje', 'fecha_envio']
    search_fields = ['nombre', 'email', 'asunto']
    list_filter = ['fecha_envio']
    actions = ['delete_selected']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            delete_selected = actions['delete_selected']
            actions['delete_selected'] = (delete_selected[0], 'delete_selected', delete_selected[2])
        return actions