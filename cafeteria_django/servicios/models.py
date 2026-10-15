from django.db import models


class Servicio(models.Model):
    CATEGORIA_CHOICES = [
        ('cafe_caliente', 'Cafés Calientes'),
        ('bebida_fria', 'Bebidas Frías'),
        ('postre', 'Postres'),
        ('desayuno', 'Desayunos'),
    ]

    titulo = models.CharField(max_length=120, verbose_name="Nombre del producto / servicio")
    contenido = models.TextField(verbose_name="Descripción")
    tipo = models.CharField(
        max_length=40,
        choices=CATEGORIA_CHOICES,
        default='cafe_caliente',
        verbose_name="Categoría",
    )
    precio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio (USD)")
    imagen_url = models.CharField(
        max_length=300,
        blank=True,
        default='',
        verbose_name="URL de imagen (opcional)",
    )
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha y hora de actualización")

    class Meta:
        verbose_name = "Servicio / Producto"
        verbose_name_plural = "Servicios / Productos"
        ordering = ['-created']

    def __str__(self):
        return f"{self.titulo} (${self.precio})"

    def obtener_imagen(self):
        if self.imagen_url:
            return self.imagen_url
        return "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=500&q=60"


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('preparando', 'En preparación'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('deuna_transferencia', 'Transferencia / Deuna'),
        ('tarjeta', 'Tarjeta'),
    ]

    MODALIDAD_CHOICES = [
        ('mesa', 'En mesa'),
        ('retiro', 'Para llevar'),
        ('domicilio', 'Domicilio'),
    ]

    cliente_nombre = models.CharField(max_length=120, verbose_name="Nombre del cliente")
    cliente_telefono = models.CharField(max_length=40, blank=True, default='', verbose_name="Teléfono")
    modalidad = models.CharField(
        max_length=30,
        choices=MODALIDAD_CHOICES,
        default='mesa',
        verbose_name="Modalidad",
    )
    mesa_o_direccion = models.CharField(max_length=200, verbose_name="Mesa o dirección")
    metodo_pago = models.CharField(
        max_length=30,
        choices=METODO_PAGO_CHOICES,
        default='efectivo',
        verbose_name="Método de pago",
    )
    referencia_pago = models.CharField(max_length=100, blank=True, default='', verbose_name="Referencia de pago")
    notas = models.TextField(blank=True, default='', verbose_name="Notas")
    resumen_pedido = models.TextField(verbose_name="Productos solicitados")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total (USD)")
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name="Estado",
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha y hora de actualización")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created']

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente_nombre} (${self.total})"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name="Pedido",
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Producto",
    )
    nombre_producto = models.CharField(max_length=120, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio unitario")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha y hora de actualización")

    class Meta:
        verbose_name = "Detalle de Pedido"
        verbose_name_plural = "Detalles de Pedidos"

    def __str__(self):
        return f"{self.cantidad}x {self.nombre_producto}"
