from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, verbose_name="Nombre de la categoría")
    descripcion = models.CharField(max_length=200, blank=True, default='', verbose_name="Descripción")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha y hora de actualización")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Post(models.Model):
    titulo = models.CharField(max_length=150, verbose_name="Título")
    subtitulo = models.CharField(max_length=200, blank=True, default='', verbose_name="Subtítulo / Oferta")
    contenido = models.TextField(verbose_name="Contenido")
    imagen_url = models.CharField(
        max_length=300,
        blank=True,
        default='',
        verbose_name="URL de imagen (opcional)",
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Autor",
    )
    categorias = models.ManyToManyField(
        Categoria,
        related_name='posts',
        verbose_name="Categorías",
    )
    etiqueta_oferta = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name="Etiqueta de oferta (ej: 2x1, -20%)",
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha y hora de actualización")

    class Meta:
        verbose_name = "Publicación del Blog"
        verbose_name_plural = "Publicaciones del Blog"
        ordering = ['-created']

    def __str__(self):
        return self.titulo

    def obtener_imagen(self):
        if self.imagen_url:
            return self.imagen_url
        return "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=500&q=60"
