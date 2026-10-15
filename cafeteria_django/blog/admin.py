from django.contrib import admin
from .models import Categoria, Post


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'created', 'updated')
    search_fields = ('nombre',)
    readonly_fields = ('created', 'updated')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'etiqueta_oferta', 'autor', 'activo', 'created', 'updated')
    list_filter = ('categorias', 'activo', 'created')
    search_fields = ('titulo', 'subtitulo', 'contenido')
    readonly_fields = ('created', 'updated')
