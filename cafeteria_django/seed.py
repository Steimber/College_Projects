import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafeteria_project.settings')
django.setup()

from django.contrib.auth.models import User
from servicios.models import Servicio, Pedido, DetallePedido
from blog.models import Categoria, Post


def run_seed():
    # 1. Crear superusuario admin / admin1234 si no existe
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@cafeteria.com', 'is_staff': True, 'is_superuser': True},
    )
    if created:
        admin_user.set_password('admin1234')
        admin_user.save()
        print("Superusuario creado: admin / admin1234")

    # 2. Crear Servicios / Productos de la cafetería
    if Servicio.objects.count() == 0:
        productos = [
            {
                'titulo': 'Café Pasado Manabita',
                'contenido': 'Café 100% arábigo pasado tradicionalmente, servido bien caliente.',
                'tipo': 'cafe_caliente',
                'precio': Decimal('1.50'),
                'imagen_url': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=500&q=60',
            },
            {
                'titulo': 'Cappuccino Artesanal',
                'contenido': 'Espresso doble con leche vaporizada cremosa y toque de canela.',
                'tipo': 'cafe_caliente',
                'precio': Decimal('2.50'),
                'imagen_url': 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?auto=format&fit=crop&w=500&q=60',
            },
            {
                'titulo': 'Frappé de Mocca y Caramelo',
                'contenido': 'Bebida fría batida con café espresso, chocolate, hielo y crema.',
                'tipo': 'bebida_fria',
                'precio': Decimal('3.25'),
                'imagen_url': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=500&q=60',
            },
            {
                'titulo': 'Cheesecake de Maracuyá',
                'contenido': 'Porción de cheesecake casero con pulpa natural de maracuyá.',
                'tipo': 'postre',
                'precio': Decimal('2.75'),
                'imagen_url': 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=500&q=60',
            },
            {
                'titulo': 'Combo Desayuno Universitario',
                'contenido': 'Bolón mixto de queso y chicharrón + taza de café pasado o jugo.',
                'tipo': 'desayuno',
                'precio': Decimal('3.50'),
                'imagen_url': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=500&q=60',
            },
        ]
        for p in productos:
            Servicio.objects.create(**p)
        print("Productos de Servicios creados.")

    # 3. Crear Categorías y Posts del Blog (Ofertas, Promociones, etc.)
    if Categoria.objects.count() == 0:
        cat_ofertas = Categoria.objects.create(
            nombre='Ofertas',
            descripcion='Descuentos especiales y rebajas de la semana en la cafetería.',
        )
        cat_promos = Categoria.objects.create(
            nombre='Promociones 2x1',
            descripcion='Promociones 2x1 para compartir en tardes de estudio.',
        )
        cat_novedades = Categoria.objects.create(
            nombre='Novedades y Menú',
            descripcion='Nuevos productos, granos de café y eventos del local.',
        )

        p1 = Post.objects.create(
            titulo='2x1 en todos los Frappés los martes y jueves',
            subtitulo='Válido de 14:00 a 18:00 presentando carnet estudiantil',
            contenido='Ven con tus compañeros de la universidad y pide dos Frappés de Mocca o Caramelo por el precio de uno.',
            etiqueta_oferta='2x1 OFERTA',
            imagen_url='https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=500&q=60',
            autor=admin_user,
        )
        p1.categorias.add(cat_ofertas, cat_promos)

        p2 = Post.objects.create(
            titulo='Oferta de la Mañana: Desayuno + Café por $3.00',
            subtitulo='Todos los días de 07:00 a 10:00 AM',
            contenido='Empieza el día con energía antes de clases con nuestro combo especial de desayuno manabita con descuento.',
            etiqueta_oferta='-15% OFF',
            imagen_url='https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=500&q=60',
            autor=admin_user,
        )
        p2.categorias.add(cat_ofertas)

        p3 = Post.objects.create(
            titulo='Nueva cosecha de café tostado de Jipijapa',
            subtitulo='Aroma intenso con notas de cacao',
            contenido='Ya tenemos disponible en barra nuestro nuevo lote de café de altura cultivado en el sur de Manabí.',
            etiqueta_oferta='NUEVO',
            imagen_url='https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=500&q=60',
            autor=admin_user,
        )
        p3.categorias.add(cat_novedades)
        print("Categorías y Posts del Blog creados.")

    # 4. Crear un Pedido de ejemplo en la pasarela
    if Pedido.objects.count() == 0:
        srv1 = Servicio.objects.first()
        if srv1:
            ped = Pedido.objects.create(
                cliente_nombre='Carlos Mendoza',
                cliente_telefono='0998765432',
                modalidad='mesa',
                mesa_o_direccion='Mesa 2',
                metodo_pago='efectivo',
                referencia_pago='Pago en caja',
                notas='Servir bien caliente',
                resumen_pedido=f"2x {srv1.titulo} (${srv1.precio * 2:.2f})",
                total=srv1.precio * 2,
                estado='pendiente',
            )
            DetallePedido.objects.create(
                pedido=ped,
                servicio=srv1,
                nombre_producto=srv1.titulo,
                cantidad=2,
                precio_unitario=srv1.precio,
                subtotal=srv1.precio * 2,
            )
            print("Pedido inicial de prueba creado.")


if __name__ == '__main__':
    run_seed()
