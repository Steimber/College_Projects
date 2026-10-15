from django.contrib import admin
from .models import Servicio, Pedido, DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('created', 'updated')


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'precio', 'disponible', 'created', 'updated')
    list_filter = ('tipo', 'disponible', 'created')
    search_fields = ('titulo', 'contenido')
    readonly_fields = ('created', 'updated')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente_nombre',
        'modalidad',
        'metodo_pago',
        'total',
        'estado',
        'created',
        'updated',
    )
    list_filter = ('estado', 'modalidad', 'metodo_pago', 'created')
    search_fields = ('cliente_nombre', 'cliente_telefono', 'resumen_pedido')
    readonly_fields = ('created', 'updated')
    inlines = [DetallePedidoInline]


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'nombre_producto', 'cantidad', 'precio_unitario', 'subtotal', 'created', 'updated')
    readonly_fields = ('created', 'updated')
