from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Servicio, Pedido, DetallePedido
from blog.models import Post, Categoria


def inicio(request):
    servicios_destacados = Servicio.objects.filter(disponible=True)[:6]
    ofertas_blog = Post.objects.filter(activo=True).prefetch_related('categorias')[:3]
    categorias_blog = Categoria.objects.all()
    total_pedidos = Pedido.objects.count()
    return render(
        request,
        'servicios/inicio.html',
        {
            'servicios': servicios_destacados,
            'ofertas_blog': ofertas_blog,
            'categorias_blog': categorias_blog,
            'total_pedidos': total_pedidos,
        },
    )


def servicios_pedidos(request):
    todos_servicios = list(Servicio.objects.filter(disponible=True))

    if request.method == 'POST':
        cliente_nombre = request.POST.get('cliente_nombre', '').strip()
        cliente_telefono = request.POST.get('cliente_telefono', '').strip()
        modalidad = request.POST.get('modalidad', 'mesa')
        mesa_o_direccion = request.POST.get('mesa_o_direccion', '').strip()
        metodo_pago = request.POST.get('metodo_pago', 'efectivo')
        referencia_pago = request.POST.get('referencia_pago', '').strip()
        notas = request.POST.get('notas', '').strip()

        items_seleccionados = []
        total_pedido = Decimal('0.00')
        resumen_lineas = []

        for srv in todos_servicios:
            cant_str = request.POST.get(f'cantidad_{srv.id}', '0').strip()
            try:
                cantidad = int(cant_str)
            except ValueError:
                cantidad = 0

            if cantidad > 0:
                subtotal = srv.precio * Decimal(cantidad)
                total_pedido += subtotal
                items_seleccionados.append((srv, cantidad, subtotal))
                resumen_lineas.append(f"{cantidad}x {srv.titulo} (${subtotal:.2f})")

        if not cliente_nombre:
            messages.error(request, "Ingresa tu nombre para registrar el pedido.")
        elif not items_seleccionados:
            messages.error(request, "Selecciona al menos 1 producto (cantidad mayor a 0).")
        else:
            pedido = Pedido.objects.create(
                cliente_nombre=cliente_nombre,
                cliente_telefono=cliente_telefono or "Sin teléfono",
                modalidad=modalidad,
                mesa_o_direccion=mesa_o_direccion or "Local",
                metodo_pago=metodo_pago,
                referencia_pago=referencia_pago or "En caja",
                notas=notas,
                resumen_pedido=" | ".join(resumen_lineas),
                total=total_pedido,
                estado='pendiente',
            )
            detalles_bulk = [
                DetallePedido(
                    pedido=pedido,
                    servicio=srv,
                    nombre_producto=srv.titulo,
                    cantidad=cantidad,
                    precio_unitario=srv.precio,
                    subtotal=subtotal,
                )
                for srv, cantidad, subtotal in items_seleccionados
            ]
            DetallePedido.objects.bulk_create(detalles_bulk)
            messages.success(request, f"Pedido #{pedido.id} guardado correctamente.")
            return redirect('servicios:pedido_confirmado', pedido_id=pedido.id)

    return render(
        request,
        'servicios/menu_pedidos.html',
        {
            'todos_servicios': todos_servicios,
        },
    )


def pedido_confirmado(request, pedido_id):
    pedido = get_object_or_404(Pedido.objects.prefetch_related('detalles'), id=pedido_id)
    return render(request, 'servicios/pedido_exito.html', {'pedido': pedido})


def panel_modificar_pagina(request):
    if request.method == 'POST':
        accion = request.POST.get('accion', '')

        if accion == 'crear_servicio':
            titulo = request.POST.get('titulo', '').strip()
            contenido = request.POST.get('contenido', '').strip()
            tipo = request.POST.get('tipo', 'cafe_caliente')
            precio_str = request.POST.get('precio', '0').strip()
            imagen_url = request.POST.get('imagen_url', '').strip()
            disponible = request.POST.get('disponible') == 'on'

            try:
                precio = Decimal(precio_str)
            except Exception:
                precio = Decimal('2.00')

            if titulo:
                Servicio.objects.create(
                    titulo=titulo,
                    contenido=contenido or "Producto de cafetería.",
                    tipo=tipo,
                    precio=precio,
                    imagen_url=imagen_url,
                    disponible=disponible,
                )
                messages.success(request, f"Producto '{titulo}' creado.")

        elif accion == 'editar_servicio':
            srv_id = request.POST.get('servicio_id')
            srv = get_object_or_404(Servicio, id=srv_id)
            srv.titulo = request.POST.get('titulo', srv.titulo).strip()
            srv.contenido = request.POST.get('contenido', srv.contenido).strip()
            srv.tipo = request.POST.get('tipo', srv.tipo)
            try:
                srv.precio = Decimal(request.POST.get('precio', str(srv.precio)).strip())
            except Exception:
                pass
            srv.imagen_url = request.POST.get('imagen_url', srv.imagen_url).strip()
            srv.disponible = request.POST.get('disponible') == 'on'
            srv.save()
            messages.success(request, f"Producto '{srv.titulo}' actualizado.")

        elif accion == 'eliminar_servicio':
            srv_id = request.POST.get('servicio_id')
            srv = get_object_or_404(Servicio, id=srv_id)
            srv.delete()
            messages.success(request, "Producto eliminado.")

        elif accion == 'cambiar_estado_pedido':
            pedido_id = request.POST.get('pedido_id')
            nuevo_estado = request.POST.get('estado', 'pendiente')
            pedido = get_object_or_404(Pedido, id=pedido_id)
            pedido.estado = nuevo_estado
            pedido.save()
            messages.success(request, f"Pedido #{pedido.id} actualizado.")

        elif accion == 'crear_categoria_blog':
            nombre = request.POST.get('nombre', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            if nombre:
                Categoria.objects.create(nombre=nombre, descripcion=descripcion)
                messages.success(request, f"Categoría '{nombre}' creada.")

        elif accion == 'crear_post_blog':
            titulo = request.POST.get('titulo', '').strip()
            subtitulo = request.POST.get('subtitulo', '').strip()
            contenido = request.POST.get('contenido', '').strip()
            etiqueta_oferta = request.POST.get('etiqueta_oferta', '').strip()
            imagen_url = request.POST.get('imagen_url', '').strip()
            categorias_ids = request.POST.getlist('categorias')

            if titulo and contenido:
                autor = request.user if request.user.is_authenticated else User.objects.first()
                post = Post.objects.create(
                    titulo=titulo,
                    subtitulo=subtitulo,
                    contenido=contenido,
                    etiqueta_oferta=etiqueta_oferta,
                    imagen_url=imagen_url,
                    autor=autor,
                    activo=True,
                )
                if categorias_ids:
                    post.categorias.set(categorias_ids)
                messages.success(request, f"Publicación '{titulo}' creada.")

        elif accion == 'eliminar_post_blog':
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            post.delete()
            messages.success(request, "Publicación eliminada.")

        return redirect('servicios:modificar_pagina')

    servicios = Servicio.objects.all()[:30]
    pedidos = Pedido.objects.prefetch_related('detalles').all()[:30]
    posts = Post.objects.prefetch_related('categorias').all()[:20]
    categorias = Categoria.objects.all()

    return render(
        request,
        'servicios/panel_admin.html',
        {
            'servicios': servicios,
            'pedidos': pedidos,
            'posts': posts,
            'categorias': categorias,
            'categorias_servicio': Servicio.CATEGORIA_CHOICES,
            'estados_pedido': Pedido.ESTADO_CHOICES,
        },
    )
