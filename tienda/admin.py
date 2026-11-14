from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Juego, Pedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'formatted_precio', 'stock', 'disponible', 'miniatura')
    list_filter = ('disponible', 'categoria')
    search_fields = ('nombre',)

    @admin.display(description='Precio')
    def formatted_precio(self, obj):
        return f"${obj.precio:,.0f}".replace(',', '.')

    @admin.display(description='Imagen')
    def miniatura(self, obj):
        if obj.imagen_caja:
            return format_html('<img src="{}" style="height: 50px; border-radius: 4px;" />', obj.imagen_caja.url)
        return "Sin imagen"

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'juego', 'nombre_comprador', 'correo_comprador', 'telefono_comprador', 'cantidad', 'fecha_pedido')
    list_filter = ('juego',)
    search_fields = ('codigo', 'nombre_comprador', 'correo_comprador')