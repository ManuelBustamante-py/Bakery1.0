from django.contrib import admin
from .models import Producto, MensajeContacto, Credenciales, Compra, DetalleCompra

# Define DetalleCompraAdmin first
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'compra', 'producto', 'cantidad', 'precio_unitario')
    list_filter = ('usuario', 'compra')
    search_fields = ('usuario__username', 'compra__id', 'producto__nombre')

# Register the models in the admin site
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

@admin.register(Credenciales)
class CredencialesAdmin(admin.ModelAdmin):
    list_display = ['username']
    search_fields = ['username']

admin.site.register(Compra)
admin.site.register(DetalleCompra, DetalleCompraAdmin)
